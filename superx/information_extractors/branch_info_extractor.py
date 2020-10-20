'''
imports
'''
#pylint: disable=import-error
import gzip
import os
import sys
import xml.etree.ElementTree as et
import logging
import requests
from bs4 import BeautifulSoup
add_to_python_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(add_to_python_path)
from models import Branch #pylint: disable=wrong-import-position
from app import supermarket_info_dictionary, session  #pylint: disable=wrong-import-position




logging.basicConfig(filename='branch-extractor.log', level=logging.INFO,
                    format='%(asctime)s: %(funcName)s: %(levelname)s: %(message)s')


class BranchExtractor:
    '''
    extracts the branches
    '''
    def __init__(self):
        self.current_super = ''

    def run_branch_extractor(self):
        """
        This method is in charge of running the branch information extractor
        It works as such:
        1. retrieves the xml file, either from link or from the zip file
        2. parses the xml file and extracts the relevant information from it
        3. creates a list of Branch objects to be committed into the db
        4. commits all the Branch objects to the db (per supermarket)
        """
        for keys in supermarket_info_dictionary:
            self.current_super = supermarket_info_dictionary[keys]

            try:
                if self.current_super['needs_web_scraping']:
                    zip_link = self.get_zip_file_link()
                    if self.current_super['need_zip_prefix']:
                        self.current_super['branch_url'] = self.current_super['branch_url'] \
                        + zip_link
                    else:
                        self.current_super['branch_url'] = zip_link

                xml_file = self.get_xml_file()
            except ConnectionError as c_e:
                logging.error(str(c_e))
                continue
            else:
                xml_info_list = self.extract_info_from_xml(xml_file)
                branch_list = self.fill_branch_table(xml_info_list)
                session.bulk_save_objects(branch_list)
                session.commit()

    def get_zip_file_link(self):
        """
        This method web scrapes the urls in url_list and creates a set of the gzip file links.
        If connection to the url failed, raises connection error
        :return: the link for the zip file
        """
        try:
            page = requests.get(self.current_super['branch_url'])
            web_scrapper = BeautifulSoup(page.content, 'html.parser')
        except requests.ConnectionError as c_e:
            raise ConnectionError(f'''Unable to retrieve zip file link
                                for {self.current_super["store_name"]}''') from c_e
        else:
            links_list = web_scrapper.find_all('a')
            zip_link = ''

            for link in links_list:
                if link.has_attr('href'):
                    https = str(link.attrs['href'])
                    if self.current_super['link_attrs_name'] in https:
                        zip_link = https
                        break

            return zip_link

    def get_xml_file(self):
        """
        This method gets the xml file from the zipfile link
        If connection to the url failed, raises connection error
        :return: the unparsed xml file
        """
        try:
            xml_file = ''
            request = requests.get(self.current_super['branch_url'])
            content = request.content

        except requests.ConnectionError as c_e:

            raise ConnectionError(f'''Unable to retrieve xml
            file for super {self.current_super["store_name"]}''') from c_e


        else:
            if self.current_super['needs_web_scraping']:
                xml_file = gzip.decompress(content).decode(self.current_super['encoding'])
            else:
                xml_file = content.decode(self.current_super['encoding'])

        return xml_file

    def extract_info_from_xml(self, xml_file):
        """
        This method parses the xml file and then
        extracts info from the xml and packs it into a tuple.
        The tuple is then placed into a list
        :param xml_file: the parsed xml file
        :return: a list of tuples containing all the relevant information
        """
        tree = et.fromstring(xml_file)
        stores = tree.find(self.current_super['attr_path'])
        attrs_dict = self.current_super['attrs']
        xml_info_list = []

        for store in stores.findall(attrs_dict['store']):
            branch_id = store.find(attrs_dict['store_id']).text
            branch_name = store.find(attrs_dict['store_name']).text
            city = store.find(attrs_dict['city']).text
            address = store.find(attrs_dict['address']).text
            if address is None or address == ' ':
                address = city
                if city is None:
                    address = 'none'
            elif city is not None:
                address = address + ' ' + city

            sub_chain_id = attrs_dict['sub_chain_id']
            if isinstance(attrs_dict['sub_chain_id'], str):
                sub_chain_id = store.find(attrs_dict['sub_chain_id']).text

            xml_info_list.append((branch_id, branch_name, address, sub_chain_id))

        return xml_info_list

    def fill_branch_table(self, xml_info_list):
        """
        This method unpacks the tuples in the xml_info_list and creates a list of Branch items
        :param xml_info_list: a list of tuples containing all relevant information
        :return: a list of Branch objects
        """
        branch_list = []

        for branch_id, branch_name, address, sub_chain_id in xml_info_list:
            branch_list.append(Branch(id=branch_id,
                                name=branch_name, address=address,
                                sub_chain_id=sub_chain_id,
                                chain_id=self.current_super['chain_id']))

        return branch_list
