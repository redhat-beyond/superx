import requests
import gzip
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from superx.app import supermarket_info_dictionary


class BranchExtractor:

    def __init__(self):
        self.current_super = ''

    def run_branch_extractor(self):
        for keys in supermarket_info_dictionary:
            self.current_super = supermarket_info_dictionary[keys]

            try:
                if self.current_super['needs_web_scraping']:
                    zip_link = self.get_zip_file_link()
                    if self.current_super['need_zip_prefix']:
                        self.current_super['branch_url'] = self.current_super['branch_url'] + zip_link
                    else:
                        self.current_super['branch_url'] = zip_link

                xml_file = self.get_xml_file()
            except ConnectionError as ce:
                # logging.error(f'Unable to extract from zip file with url: {zip_link}')
                continue
            else:
                self.extract_info(xml_file)

    def get_zip_file_link(self):
        """
        This method web scrapes the urls in url_list and creates a set of the gzip file links.
        The method then sends the set to parsing
        If connection to the url failed, moves on to next url
        :param url_list: list of urls to extract zip files from

        """
        try:
            page = requests.get(self.current_super['branch_url'])
            web_scrapper = BeautifulSoup(page.content, 'html.parser')
        except Exception:
            raise ConnectionError(f'Unable to retrieve zip file link for {self.current_super["store_name"]}')
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
        try:
            xml_file = ''
            request = requests.get(self.current_super['branch_url'])
            content = request.content
        except Exception:
            raise ConnectionError(f'Unable to retrieve xml file for super {self.current_super["store_name"]}')
        else:
            if self.current_super['needs_web_scraping']:
                xml_file = gzip.decompress(content).decode(self.current_super['encoding'])
            else:
                xml_file = content.decode(self.current_super['encoding'])

        return xml_file

    def extract_info(self, xml_file):
        tree = ET.fromstring(xml_file)
        stores = tree.find(self.current_super['attr_path'])
        attrs_dict = self.current_super['attrs']

        for store in stores.findall(attrs_dict['store']):
            branch_id = store.find(attrs_dict['store_id']).text
            branch_name = store.find(attrs_dict['store_name']).text
            # subChainID = store.find('SUBCHAINID').text
            city = store.find(attrs_dict['city']).text
            address = store.find(attrs_dict['address']).text
            if address is None or address == ' ':
                address = city
                if city is None:
                    address = 'none'
            elif city is not None:
                address = address + ' ' + city

            print(branch_id + " " + branch_name + " " + address)

        #     branches_list.append(Branch(id=branchID, name=branchName, address=city + ", " + address,
        #                                 sub_chin_id=subChainID, sub_chin_name=subChain, chain_id=chainID))
        #
        # # Add to DB
        # db.session.add_all(branches_list)
        # db.session.commit()