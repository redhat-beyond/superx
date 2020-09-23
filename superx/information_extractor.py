import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gzip
import xml.etree.ElementTree as ET
from models import *
from app import db


class info_extractor:
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
        # url list with category PriceFull
        self.url_list = ['http://publishprice.mega.co.il/%s' % datetime.today().strftime('%Y%m%d'),
                         # mega link with correct date
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=1',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=2',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=3',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=4',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=5',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=6',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=7',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=8',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=9',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=10',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=11',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=12',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=13',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=14',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=15',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=16',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=17',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=18',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=19',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=20',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=21',
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=22',
                         # shufersal
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=23',
                         'http://matrixcatalog.co.il/NBCompetitionRegulations.aspx'  # victory
                         ]
        # current supermarket name
        self.super_name = ''
        # db.create_all()
        # db.session.commit()

    def get_zip_file_links(self):
        """
        This method web scrapes the urls in url_list and creates a set of the gzip file links.
        The method then updates super_name and sends the set to parsing
        """
        for url in self.url_list:
            page = requests.get(url)
            web_scrapper = BeautifulSoup(page.content, 'html.parser')
            links_list = web_scrapper.find_all('a')
            zip_links = set()

            for link in links_list:
                if link.has_attr('href'):
                    https = str(link.attrs['href'])
                    if 'PriceFull' in https:
                        zip_links.add(https)

            self.update_super_name(url)
            self.info_parser(zip_links)

    def info_parser(self, zip_links):
        """
        This method retrieves the xml file in the gzip file and parses it into an xml tree
        The branch_id is retrieved from the xml file and then it is sent for retrieval of the item information
        :param zip_links: list of zip file links from the website
        """
        for zip_link in zip_links:
            # corrects the urls
            if self.super_name == 'mega':
                zip_link = self.url_list[0] + '/' + zip_link
            elif self.super_name == 'victory':
                zip_link = 'http://matrixcatalog.co.il/' + zip_link

            request = requests.get(zip_link)
            content = request.content
            xml_file = gzip.decompress(content).decode('utf-8')
            # parses the xml document into a tree
            tree = ET.fromstring(xml_file)
            # gets the branch/store ID of current xml file
            branch_id = self.get_branch_id(tree.getchildren())
            # gets child containing item information
            items = tree.getchildren()[-1]
            self.extract_information(items, branch_id)

    def extract_information(self, items, current_branch_id):
        """
        This method iterates over all items in the supermarket and extracts the relevant data
        The data is then committed into the relevant table in the data base
        :param items: The child of the parsed xml tree containing all item information
        :param current_branch_id: id of current branch
        """
        # products_list = []
        # branch_price_list = []
        item = 'Item'
        bIsWeighted = 'bIsWeighted'

        # different supermarkets use different titles
        if self.super_name == 'victory':
            item = 'Product'
            bIsWeighted = 'BisWeighted'

        for item in items.findall(item):
            item_code = int(item.find('ItemCode').text)
            name = item.find('ItemName').text
            quantity = float(item.find('Quantity').text)
            price = float(item.find('ItemPrice').text)
            update_date = self.standardize_date(item.find('PriceUpdateDate').text)
            is_weighted = False
            if int(item.find(bIsWeighted).text) == 1:
                is_weighted = True

            unit_of_measure = 'none'
            if is_weighted:
                unit_of_measure = self.convert_unit_name(item.find('UnitQty').text)

            # if item already in db then continue to next item
            if Product.query.get(item_code):
                continue

            # adding current_product to the db and commit
            current_product = Product(id=item_code, name=name, quantity=quantity, is_weighted=is_weighted,
                                      unit_of_measure=unit_of_measure)
            db.session.add(current_product)
            db.session.commit()

            # adding current_branch_price to the db and commit
            current_branch_price = BranchPrice(item_code=current_product.id, price=price, update_date=update_date)
            db.session.add(current_branch_price)
            db.session.commit()

    def get_branch_id(self, tree_children_list):
        """
        Gets branch id from a parsed xml tree
        :param tree_children_list: list of the children of the root
        :return: the branch id
        """
        for child in tree_children_list:
            if child.tag == 'StoreId':
                return child.text

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
            'מ"ל': ['מיליליטרים', 'מ"ל', 'מיליליטר']
        }

        for unit in unit_dict.keys():
            if unit_in_hebrew in unit:
                return unit

        return unit_in_hebrew

    def standardize_date(self, date):
        """
        This method standardizes the update date of the item
        :param date: string representation of the date from the xml file
        :return: standardized date as a string
        """
        # remove time from date
        date = date[:10]
        # set the format according to the supermarket
        shuf_mega_format = '%Y-%m-%d'
        victory_format = '%Y/%m/%d'
        date_format = shuf_mega_format
        if self.super_name == 'victory':
            date_format = victory_format

        new_date = datetime.strptime(date, date_format).date()
        return new_date.__str__()

    def update_super_name(self, url):
        """
        This method updates the super name according to the link
        :param url: url of the current supermarket
        """
        if 'mega' in url:
            self.super_name = 'mega'
        elif 'shufersal' in url:
            self.super_name = 'shufersal'
        elif 'matrix' in url:
            self.super_name = 'victory'

p = info_extractor()
p.get_zip_file_links()
