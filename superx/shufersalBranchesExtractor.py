import requests
import gzip
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from superx.models.__init__ import Branch
from superx.app import db

# Branches file location (Shufersal only for now)
url = 'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=5&storeId=0&page=1'

# Connect to the page
page = requests.get(url)

# Parse it to html element
readPage = BeautifulSoup(page.content, 'html.parser')

# Get all links and find gz one
links = readPage.find_all('a')

branches_list = []

for link in links:
    gzLink = str(link.attrs['href'])
    if 'gz' in gzLink:
        # Get stores file and unzip it
        zipFile = requests.get(gzLink)
        unzip = gzip.decompress(zipFile.content)
        tree = ET.fromstring(str(unzip, 'utf-8'))
        chainID = tree.getchildren()[0].getchildren()[0]
        stores = tree.getchildren()[0].getchildren()[1]
        for i in stores.findall('STORE'):
            branchID = i.find('STOREID').text
            branchName = i.find('STORENAME').text
            subChainID = i.find('SUBCHAINID').text
            subChain = i.find('SUBCHAINNAME').text
            city = i.find('CITY').text
            address = i.find('ADDRESS').text
            branches_list.append(Branch(id=branchID, name=branchName, address=city + ", " + address,
                                        sub_chin_id=subChainID, sub_chin_name=subChain, chain_id=chainID))

        # Add to DB
        db.session.add_all(branches_list)
        db.session.commit()
