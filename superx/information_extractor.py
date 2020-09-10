
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
import time

# url list with category PriceFull
url_list = ['http://publishprice.mega.co.il/%s' % datetime.today().strftime('%Y%m%d'),  # mega link with correct date
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
super_name = ''
# connects to relevant sql database
conn = mysql.connector.connect(user='root', password='', host='localhost', database='testdb')
# cursor for db
cursor = conn.cursor()


def get_zip_file_links():
    """
    web scrapes the urls in url_list and gets the links for the xml files
    :return: a list of links to the zip files
    """
    for url in url_list:
        page = requests.get(url)
        web_scrapper = BeautifulSoup(page.content, 'html.parser')
        links_list = web_scrapper.find_all('a')
        zip_links = set()

        for link in links_list:
            if link.has_attr('href'):
                https = str(link.attrs['href'])
                if 'PriceFull' in https:
                    zip_links.add(https)

        global super_name
        if 'mega' in url:
            super_name = 'mega'
        elif 'shufersal' in url:
            super_name = 'shufersal'
        elif 'matrix' in url:
            super_name = 'victory'

        info_parser(zip_links)


def info_parser(zip_links):
    """
    parses info for supermarket
    :param zip_links: list of zip file links from the website
    """
    i = 0
    for zip_link in zip_links:
        # corrects the urls
        if super_name == 'mega':
            zip_link = url_list[0] + '/' + zip_link
        elif super_name == 'victory':
            zip_link = 'http://matrixcatalog.co.il/' + zip_link

        request = requests.get(zip_link)
        content = request.content
        xml_file = gzip.decompress(content).decode('utf-8')
        # parses the xml document into a tree
        tree = ET.fromstring(xml_file)
        # gets relevant child
        items = tree.getchildren()[-1]
        extract_information(items)
        # break  # only use 1 link:



def extract_information(items):
    item = ''
    if super_name == 'victory':
        item = 'Product'
    else:
        item = 'Item'

    for item in items.findall(item):
        code = int(item.find('ItemCode').text)
        name = item.find('ItemName').text
        price = item.find('ItemPrice').text
        try:
            item_id = item.find('ItemId').text
        except AttributeError:
            item_id = 0

        item_info_formula = """INSERT INTO item_info (itemCode,itemId,itemName, itemPrice) VALUES(%s,%s,%s,%s) ON DUPLICATE KEY UPDATE itemPrice = %s"""
        price_table_shufersal = """INSERT INTO price_table (itemCode, shufersal) VALUES(%s, %s)  ON DUPLICATE KEY UPDATE shufersal = %s """
        price_table_mega = """INSERT INTO price_table (itemCode, mega) VALUES(%s, %s)  ON DUPLICATE KEY UPDATE mega = %s"""

        # places the info into the the item_info table
        cursor.execute(item_info_formula, (code, item_id, name, price, price))
        conn.commit()

        # places the info into the price_table, according to the supermarket
        if super_name == 'mega':
            cursor.execute(price_table_mega, (code, price, price))
        elif super_name == 'shufersal':
            cursor.execute(price_table_shufersal, (code, price, price))
        conn.commit()

