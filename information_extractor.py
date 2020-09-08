
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

# url list with category PriceFull
url_list = ['http://publishprice.mega.co.il/%s' % datetime.today().strftime('%Y%m%d'),  # mega link with correct date
            'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC',  # shufersal
            ]

current_url_index = 0

# connects to relevant sql database
conn = mysql.connector.connect(user='root', password='', host='localhost', database='testdb')
# cursor for db
cursor = conn.cursor()


def get_xml_file_links():
    """
    web scrapes the urls in url_list and gets the links for the xml files
    :return: a list of links to the zip files
    """
    for url in url_list:
        page = requests.get(url)
        web_scrapper = BeautifulSoup(page.content, 'html.parser')
        links_list = web_scrapper.find_all('a')
        zip_links = []

        for link in links_list:
            https = str(link.attrs['href'])
            if 'PriceFull' in https:
                zip_links.append(https)

        if 'mega' or 'shufersal' in url:
            mega_and_shufersal_info_parser(zip_links)

        global current_url_index
        current_url_index = 1


def mega_and_shufersal_info_parser(zip_links):
    """
    parses info for mega and shufersal supermarket
    :param zip_links: list of zip file links from the website
    """
    for zip_link in zip_links:
        # corrects the mega url
        if 'http' not in zip_link:
            zip_link = url_list[0] + '/' + zip_link

        request = requests.get(zip_link)
        xml_file = gzip.decompress(request.content)
        # parses the xml document into a tree
        tree = ET.fromstring(str(xml_file, 'utf-8'))
        # gets relevant child
        items = tree.getchildren()[-1]
        extract_information(items)
        break  # only use 1 link from each url


def extract_information(items):
    for item in items.findall('Item'):
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
        if current_url_index == 0:
            cursor.execute(price_table_mega, (code, price, price))
        elif current_url_index == 1:
            cursor.execute(price_table_shufersal, (code, price, price))
        conn.commit()

