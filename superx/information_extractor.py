import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gzip
import xml.etree.ElementTree as ET
from models import Product, BranchPrice
from app import db
import logging


logging.basicConfig(filename='test.log', level=logging.INFO,
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
        self.super_specific_information = {'mega': {'store_name': 'mega',
                                                    'url': f'http://publishprice.mega.co.il/{str(datetime.today().strftime("%Y%m%d"))}',
                                                    'multiple_pages': False,
                                                    'zip_link_prefix': f'http://publishprice.mega.co.il/{str(datetime.today().strftime("%Y%m%d"))}/',
                                                    'item_attr_name': 'Item',
                                                    'is_weighted_attr_name': 'bIsWeighted',
                                                    'item_date_format': '%Y-%m-%d'},
                                           'shufersal': {'store_name': 'shufersal',
                                                         'url': 'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=1',
                                                         'multiple_pages': True,
                                                         'zip_link_prefix': None,
                                                         'item_attr_name': 'Item',
                                                         'is_weighted_attr_name': 'bIsWeighted',
                                                         'item_date_format': '%Y-%m-%d'},
                                           'matrix': {'store_name': 'victory',
                                                      'url': 'http://matrixcatalog.co.il/NBCompetitionRegulations.aspx',
                                                      'multiple_pages': False,
                                                      'zip_link_prefix': 'http://matrixcatalog.co.il/',
                                                      'item_attr_name': 'Product',
                                                      'is_weighted_attr_name': 'BisWeighted',
                                                      'item_date_format': '%Y-%m-%d'}
                                           }

    def run_extractor(self):
        """
        This method starts the extraction process
        """
        for key in self.super_specific_information:
            self.current_super = self.super_specific_information[key]
            url_list = [self.current_super['url']]

            if self.current_super['multiple_pages']:
                try:
                    url_list = self.get_all_super_links()
                except ConnectionError as ce:
                    logging.error(str(ce))

            self.get_zip_file_links(url_list)

    def get_zip_file_links(self, url_list):
        """
        This method web scrapes the urls in url_list and creates a set of the gzip file links.
        The method then sends the set to parsing
        If connection to the url failed, moves on to next url
        :param url_list: list of urls to extract zip files from

        """
        for url in url_list:
            try:
                page = requests.get(url)
                web_scrapper = BeautifulSoup(page.content, 'html.parser')
            except Exception:
                logging.error(f'Unable to connect to url:\n{url}')
            else:
                links_list = web_scrapper.find_all('a')
                zip_links = set()

                for link in links_list:
                    if link.has_attr('href'):
                        https = str(link.attrs['href'])
                        if 'PriceFull' in https:
                            zip_links.add(https)

                self.info_parser(zip_links)

    def info_parser(self, zip_links):
        """
        This method retrieves the xml file in the gzip file and parses it into an xml tree
        The branch_id is retrieved from the xml file and then it is sent for retrieval of the item information
        If connection failed, moves on to next link
        :param zip_links: list of zip file links from the website
        """
        for zip_link in zip_links:
            # fix zip link url if neccessary
            if not self.current_super['zip_link_prefix'] is None:
                zip_link = self.current_super['zip_link_prefix'] + zip_link

            try:
                request = requests.get(zip_link)
                content = request.content
            except Exception:
                logging.error(f'Unable to extract from zip file with url: {zip_link}')
            else:
                xml_file = gzip.decompress(content).decode('utf-8')
                # parses the xml document into a tree
                tree = ET.fromstring(xml_file)
                # gets child containing item information
                items = tree.getchildren()[-1]
                self.extract_information(items)

    def extract_information(self, items):
        """
        This method iterates over all items in the supermarket and extracts the relevant data
        The data is then committed into the relevant table in the data base
        :param items: The child of the parsed xml tree containing all item information
        """
        item_attr_name = self.current_super['item_attr_name']
        bIsWeighted = self.current_super['is_weighted_attr_name']

        for item in items.findall(item_attr_name):
            item_code = int(item.find('ItemCode').text)
            name = item.find('ItemName').text
            # exclude unwanted names from DB
            for exclude in self.exclude_names:
                if exclude in name:
                    continue

            quantity = float(item.find('Quantity').text)
            price = float(item.find('ItemPrice').text)
            update_date = self.standardize_date(item.find('PriceUpdateDate').text)
            is_weighted = False
            if item.find(bIsWeighted).text == '1':
                is_weighted = True

            unit_of_measure = self.convert_unit_name(item.find('UnitQty').text)
            # if item already in db then continue to next item
            if bool(Product.query.filter_by(id=item_code).first()):
                # adding current_branch_price to the db and commit
                current_branch_price = BranchPrice(item_code=item_code, price=price, update_date=update_date)
                db.session.add(current_branch_price)
                db.session.commit()
                continue

            # adding current_product to the db and commit
            current_product = Product(id=item_code, name=name, quantity=quantity, is_weighted=is_weighted,
                                      unit_of_measure=unit_of_measure)
            db.session.add(current_product)
            db.session.commit()
            # adding current_branch_price to the db and commit
            current_branch_price = BranchPrice(item_code=item_code, price=price, update_date=update_date)
            db.session.add(current_branch_price)
            db.session.commit()

    def convert_unit_name(self, unit_in_hebrew):
        """
        This method standardizes the unit of measurement
        if the unit of measurement is not know, returns unknown
        :param unit_in_hebrew: unit of measurement in hebrew
        :return: standardized version of the unit or unknown if the unit is not known
        """
        unit_dict = {
            'ק"ג': ['קילו', 'ק"ג', 'קילו', 'קילוגרמים'],
            'גרם': ['גרם', 'גרמים'],
            'ליטר': ['ליטר', 'ליטרים', 'ליטר    '],
            'מ"ל': ['מיליליטרים', 'מ"ל', 'מיליליטר'],
            'אין': ['יחידה', 'לא ידוע']
        }

        for unit in unit_dict.keys():
            if unit_in_hebrew in unit_dict[unit]:
                return unit

        # as a default return the original unit and log it
        logging.info(f'New item weight name encoded to UTF-8: {unit_in_hebrew.encode("UTF-8")}')
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
            raise ConnectionError(f'Unable to connect to url to find number of pages for {self.current_super["store_name"]}')

        general_url = self.current_super['url']
        general_url = general_url[:len(general_url)-1]
        url_list = []

        for i in range(1, num_of_pages + 1):
            url_list.append(general_url + str(i))

        return url_list

    def get_num_of_pages(self):
        """
        gets the number of pages for a certain supermarket
        In case the number of pages increases or decreases the code will always check if it is a single, double, triple digit
        :return: number of pages
        """
        num_of_pages = '1'
        try:
            page = requests.get(self.current_super['url'])
            web_scrapper = BeautifulSoup(page.content, 'html.parser')
        except Exception:
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
