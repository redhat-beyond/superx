'''
imports
'''
import os
import sys
from datetime import datetime
import gzip
import logging
import xml.etree.ElementTree as ET
from decimal import Decimal
from bs4 import BeautifulSoup # pylint: disable=import-error
import requests # pylint: disable=import-error
add_to_python_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(add_to_python_path)
from app import supermarket_info_dictionary, session # pylint: disable=import-error disable=wrong-import-position
from models import Product, BranchPrice # pylint: disable=import-error disable=wrong-import-position


logging.basicConfig(filename='info-extractor.log', level=logging.INFO,
                    format='%(asctime)s: %(funcName)s: %(levelname)s: %(message)s')


class InfoExtractor:
    """
    This class executes the following task:
        1. web scrapes the url's from the url list and retrieves the relevant gzip file links
        2. extracts the xml file from the gzip file and parses it into an xml tree
        3. the relevant information is then extracted from the parsed xml tree
        4. the information is placed in the relevant table in the db.
            - this script only updates the product information (db table name = products)
            - and branch price information (db table name = branch_price)

        Currently this class can only handle the supermarkets: shufersal, mega and victory
        XML files are found @https://www.consumers.org.il/item/transparency_price
    """

    def __init__(self):
        self.current_super = ''
        # list of unwanted names to be filter out
        self.exclude_names = ['משלוחים', 'ריק', 'פיקדון', 'תיבה', 'משלוח']
        self.item_id_set = set()

    def run_info_extractor(self):
        """
        This method is incharge of the whole extraction process.
        It works in the following way:
        1. retreives all zip file links from the relevant website
        2. retreives all branch id's and child node objects that hold the wanted information
        3. creates 2 lists one containing all Product info and the other all BranchPrice info
        4. commits to the db
        """
        for key in supermarket_info_dictionary:
            self.current_super = supermarket_info_dictionary[key]
            url_list = [self.current_super['url']]

            if self.current_super['multiple_pages']:
                try:
                    url_list = self.get_all_super_links()
                except ConnectionError as c_e:
                    logging.error(str(c_e))

            zip_links = self.get_zip_file_links(url_list)
            node_info_list = self.extract_xml_from_zip_and_parse(zip_links)

            for info_child_node, branch_id in node_info_list:
                xml_info_list = self.extract_information_from_parsed_xml(info_child_node)
                if branch_id == '86' and self.current_super['store_name'] == 'victory':
                    continue
                product_info_list, branch_price_list = self.fill_product_and_branch_price_tables(
                    xml_info_list,
                    branch_id)
                session.bulk_save_objects(product_info_list)
                session.bulk_save_objects(branch_price_list)
                session.commit()

    def get_zip_file_links(self, url_list):
        """
        This method web scrapes the urls in url_list and creates a set of the gzip file links.
        The method then sends the set to parsing
        If connection to the url failed, moves on to next url
        :param url_list: list of urls to extract zip files from
        :return: a set of zip file links

        """
        for url in url_list:
            try:
                page = requests.get(url)
                web_scrapper = BeautifulSoup(page.content, 'html.parser')
            except requests.ConnectionError:
                logging.error('Unable to connect to url:\n %s', url)
            else:
                links_list = web_scrapper.find_all('a')
                zip_links = set()

                for link in links_list:
                    if link.has_attr('href'):
                        https = str(link.attrs['href'])
                        if self.current_super['price_full'] in https:
                            zip_links.add(https)

                return zip_links

    def extract_xml_from_zip_and_parse(self, zip_links):
        """
        This method retrieves the xml file in the gzip file and parses it into an xml tree
        The child node containg the item information is found
        and The branch_id is retrieved from the xml file.
        This information is packed into a tuple and placed in a list
        If connection failed, moves on to next link
        :param zip_links: list of zip file links from the website
        :return: a list of tuples containing all branch id's and child node object's
        """
        node_info_list = []

        for zip_link in zip_links:
            # fix zip link url if neccessary
            if not self.current_super['zip_link_prefix'] is None:
                zip_link = self.current_super['zip_link_prefix'] + zip_link

            try:
                request = requests.get(zip_link)
                content = request.content
            except requests.ConnectionError:
                logging.error('Unable to extract from zip file with url: %s', zip_link)
            else:
                xml_file = gzip.decompress(content).decode('utf-8')
                store_id = 'StoreId'
                if self.current_super['store_name'] == 'victory':
                    store_id = 'StoreID'

                # parses the xml document into a tree
                tree = ET.fromstring(xml_file)
                branch_id = tree.find(store_id).text.lstrip('0')
                # gets child containing item information
                info_child_node = tree.getchildren()[-1]  #pylint: disable=deprecated-method
                node_info_list.append((info_child_node, branch_id))

        return node_info_list

    def extract_information_from_parsed_xml(self, xml_info_child_node):
        """
        This method iterates over all items in the supermarket and extracts the relevant data
        The data is then committed packed into a tuple and placed in a list of all the info tuples
        :param xml_info_child_node: The child of the parsed xml tree containing all item information
        :return: a list of tuples containing the information
        """
        item_attr_name = self.current_super['item_attr_name']
        is_weighted_attr = self.current_super['is_weighted_attr_name']
        xml_info_list = []

        for item in xml_info_child_node.findall(item_attr_name):
            item_code = int(item.find('ItemCode').text)
            if item_code == 0:
                continue

            item_name = item.find('ItemName').text
            # exclude unwanted names from DB
            for name in self.exclude_names:
                if name in item_name:
                    continue

            quantity = Decimal(item.find('Quantity').text)
            price = Decimal(item.find('ItemPrice').text)
            update_date = self.standardize_date(item.find('PriceUpdateDate').text)
            is_weighted = False
            if item.find(is_weighted_attr).text == '1':
                is_weighted = True

            unit_of_measure = 'אין'
            if is_weighted:
                unit_of_measure = self.standardize_weight_name(item.find('UnitQty').text.strip())

            xml_info_list.append(
            (item_code, item_name, quantity, is_weighted, unit_of_measure, price, update_date))

        return xml_info_list

    def fill_product_and_branch_price_tables(self, information_list, branch_id):
        """
        This method receives a list containing a tuple of all the xml info
        and places it into the correct table
        :param information_list: list of tuples containing all the xml info
        :param branch_id: the id of the current branch
        :return: two lists, one containing Product obj the other BranchPrice objects
        """
        branch_price_list = []
        product_info_list = []

        for item_code, item_name, quantity, is_weighted, unit_of_measure, price, update_date in information_list: # pylint: disable=line-too-long
            # If the item is in the db , skip it
            if item_code not in self.item_id_set:
                product_info_list.append(Product(id=item_code, name=item_name, quantity=quantity,
                                                 is_weighted=is_weighted,
                                                 unit_of_measure=unit_of_measure))
                self.item_id_set.add(item_code)

            branch_price_list.append(BranchPrice(chain_id=self.current_super['chain_id'],
                                                branch_id=branch_id,
                                                item_code=item_code, price=price,
                                                update_date=update_date))

        return product_info_list, branch_price_list

    def standardize_weight_name(self, unit_in_hebrew): #pylint: disable=no-self-use
        """
        This method standardizes the unit of measurement
        if the unit of measurement is not know, returns unknown
        :param unit_in_hebrew: unit of measurement in hebrew
        :return: standardized version of the unit or unknown if the unit is not known
        """
        unit_dict = {
            'ק"ג': ['קילו', 'ק"ג', 'קילו', 'קילוגרמים', '1 ק"ג'],
            'גרם': ['גרם', 'גרמים'],
            'ליטר': ['ליטר', 'ליטרים', 'ליטר    '],
            'מ"ל': ['מיליליטרים', 'מ"ל', 'מיליליטר'],
            'אין': ['יחידה', 'לא ידוע', "יח'", "'יח", "יח`", "מטרים", "מארז", "קרטון"]
        }

        for unit in unit_dict.keys(): #pylint: disable=C0201
            if unit_in_hebrew in unit_dict[unit]:
                return unit

        if "יח'" in unit_in_hebrew:
            return 'אין'

        # as a default return the original unit and log it
        logging.info('New item weight name encoded to UTF-8: %s', unit_in_hebrew.encode("UTF-8"))

        return unit_in_hebrew

    def standardize_date(self, date):
        """
        This method standardizes the update date of the item
        :param date: string representation of the date from the xml file
        :return: standardized date as a string
        """
        # remove time from date
        date = date[:10]
        date_format = self.current_super['item_date_format']
        new_date = datetime.strptime(date, date_format).date()

        return new_date.__str__()

    def get_all_super_links(self):
        """
        builds a list of urls for the supermarket
        :return: a list of links according to th amount of pages
        """
        num_of_pages = self.get_num_of_pages()
        if num_of_pages == -1:
            raise ConnectionError(
                f'''Unable to connect to url to find number of pages for
                {self.current_super["store_name"]}''')

        general_url = self.current_super['url']
        general_url = general_url[:len(general_url) - 1]
        url_list = []

        for i in range(1, num_of_pages + 1):
            url_list.append(general_url + str(i))

        return url_list

    def get_num_of_pages(self):
        """
        gets the number of pages for a certain supermarket
        In case the number of pages increases or decreases
        the code will always check if it is a single, double, triple digit
        :return: number of pages
        """
        num_of_pages = '1'
        try:
            page = requests.get(self.current_super['url'])
            web_scrapper = BeautifulSoup(page.content, 'html.parser')
        except requests.ConnectionError:
            num_of_pages = -1
        else:
            if self.current_super['store_name'] == 'shufersal':
                links = web_scrapper.find_all(name='a', text='>>')
                wanted_link = links[0]

                for i in range(1, 4):
                    try:
                        num_of_pages = int(wanted_link.attrs['href'][-i::])
                    except ValueError:
                        break

        return num_of_pages
