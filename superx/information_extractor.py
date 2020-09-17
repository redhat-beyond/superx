
'''
    This is in charge of extracting the XML document
    XML files are found @ https://www.consumers.org.il/item/transparency_price
'''
import mysql.connector
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gzip
import xml.etree.ElementTree as ET
from superx.app import db


class info_extractor:

    def __init__(self):
        # url list with category PriceFull
        self.url_list = ['http://publishprice.mega.co.il/%s' % datetime.today().strftime('%Y%m%d'),  # mega link with correct date
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
                         'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=22',  # shufersal
                         'http://matrixcatalog.co.il/NBCompetitionRegulations.aspx'      # victory
                         ]
        # current supermarket name
        self.super_name = ''
        # connects to relevant sql database
        self.conn = mysql.connector.connect(user='root', password='zaq1xsw2', host='localhost', database='testdb')
        # cursor for db
        self.cursor = self.conn.cursor()

    def get_zip_file_links(self):
        """
        web scrapes the urls in url_list and gets the links for the xml files
        :return: a list of links to the zip files
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

            if 'mega' in url:
                self.super_name = 'mega'
            elif 'shufersal' in url:
                self.super_name = 'shufersal'
            elif 'matrix' in url:
                self.super_name = 'victory'

            self.info_parser(zip_links)

    def info_parser(self, zip_links):
        """
        parses info for supermarket
        :param zip_links: list of zip file links from the website
        """
        i = 0
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
            # gets relevant child
            items = tree.getchildren()[-1]
            self.extract_information(items, branch_id)
            # break  # only use 1 link:

    def extract_information(self, items, current_branch_id):
        item = 'Item'
        bIsWeighted = 'bIsWeighted'

        # different supermarkets use different titles
        if self.super_name == 'victory':
            item = 'Product'
            bIsWeighted = 'BisWeighted'

        for item in items.findall(item):
            code = int(item.find('ItemCode').text)
            name = item.find('ItemName').text
            quantity = item.find('Quantity').text
            price = item.find('ItemPrice').text
            is_weighted = False
            if item.find(bIsWeighted).text == 1:
                is_weighted = True

            unit_of_measure = 'none'
            if is_weighted:
                unit_of_measure = self.convert_unit_name(item.find('UnitQty').text)

            try:
                item_id = item.find('ItemId').text
            except AttributeError:
                item_id = 0

            item_info_formula = """INSERT INTO item_info (itemCode,itemId,itemName) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE itemName = itemName """
            price_table_shufersal = """INSERT INTO price_table (itemCode, shufersal) VALUES(%s, %s)  ON DUPLICATE KEY UPDATE shufersal = %s """
            price_table_mega = """INSERT INTO price_table (itemCode, mega) VALUES(%s, %s)  ON DUPLICATE KEY UPDATE mega = %s """

            # places the info into the the item_info table
            self.cursor.execute(item_info_formula, (code, item_id, name))
            self.conn.commit()

            # places the info into the price_table, according to the supermarket
            if self.super_name == 'mega':
                self.cursor.execute(price_table_mega, (code, price, price))
            elif self.super_name == 'shufersal':
                self.cursor.execute(price_table_shufersal, (code, price, price))
            self.conn.commit()

    def get_branch_id(self, tree_children_list):
        """ Gets branch id from a parsed xml tree"""
        for child in tree_children_list:
            if child.tag == 'StoreId':
                return child.text

    def convert_unit_name(self, unit_in_hebrew):
        """method to convert hebrew measurement to english measurement"""
        unit_dict = {
            'kg': ['קילו', 'ק"ג', 'קילו', 'קילוגרמים'],
            'gram': ['גרם', 'גרמים'],
            'liter': ['ליטר', 'ליטרים', 'ליטר    '],
            'milliliter': ['מיליליטרים', 'מ"ל', 'מיליליטר']
            }

        for unit in unit_dict.keys():
            if unit_in_hebrew in unit:
                return unit

        return 'none'
