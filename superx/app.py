from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from os import environ, path
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

app.config.from_object('config.BaseConfig')
app.config['SECRET_KEY'] = 'aefguhw49t23465'
app.config['TESTING'] = False
FLASK_APP = environ.get('FLASK_APP')
FLASK_ENV = environ.get('FLASK_ENV')

# Database
SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(app)
db.init_app(app)

dictionary for information extractors
supermarket_info_dictionary = {'mega': {'store_name': 'mega',
                                        'url': f'http://publishprice.mega.co.il/{str(datetime.today().strftime("%Y%m%d"))}',
                                        'multiple_pages': False,
                                        'zip_link_prefix': f'http://publishprice.mega.co.il/{str(datetime.today().strftime("%Y%m%d"))}/',
                                        'item_attr_name': 'Item',
                                        'price_full': 'PriceFull',
                                        'is_weighted_attr_name': 'bIsWeighted',
                                        'item_date_format': '%Y-%m-%d',
                                        'branch_url': f'http://publishprice.mega.co.il/{str(datetime.today().strftime("%Y%m%d"))}/Stores7290055700007-{str(datetime.today().strftime("%Y%m%d"))}0001.xml',
                                        'needs_web_scraping': False,
                                        'need_zip_prefix': False,
                                        'encoding': 'UTF-16',
                                        'link_attrs_name': None,
                                        'attr_path': 'SubChains/SubChain/Stores',
                                        'chain_id': 7290055700007,
                                        'attrs': {'store': 'Store',
                                                  'store_id': 'StoreId',
                                                  'store_name': 'StoreName',
                                                  'address': 'Address',
                                                  'city': 'City'}
                                        },
                               'shufersal': {'store_name': 'shufersal',
                                             'url': 'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=0&sort=Category&sortdir=ASC&page=1',
                                             'multiple_pages': True,
                                             'zip_link_prefix': None,
                                             'item_attr_name': 'Item',
                                             'price_full': 'PriceFull',
                                             'is_weighted_attr_name': 'bIsWeighted',
                                             'item_date_format': '%Y-%m-%d',
                                             'branch_url': 'http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=5&storeId=0&page=1',
                                             'needs_web_scraping': True,
                                             'need_zip_prefix': False,
                                             'encoding': 'UTF-8',
                                             'link_attrs_name': 'Stores7290027600007',
                                             'attr_path': '{http://www.sap.com/abapxml}values/STORES',
                                             'chain_id': 7290027600007,
                                             'attrs': {'store': 'STORE',
                                                       'store_id': 'STOREID',
                                                       'store_name': 'STORENAME',
                                                       'address': 'ADDRESS',
                                                       'city': 'CITY'}
                                             },
                               'victory': {'store_name': 'victory',
                                           'url': 'http://matrixcatalog.co.il/NBCompetitionRegulations.aspx',
                                           'multiple_pages': False,
                                           'zip_link_prefix': 'http://matrixcatalog.co.il/',
                                           'item_attr_name': 'Product',
                                           'price_full': 'PriceFull7290696200003',
                                           'is_weighted_attr_name': 'BisWeighted',
                                           'item_date_format': '%Y-%m-%d',
                                           'branch_url': 'http://matrixcatalog.co.il/',
                                           'needs_web_scraping': True,
                                           'need_zip_prefix': True,
                                           'encoding': 'UTF-8',
                                           'link_attrs_name': 'StoresFull7290696200003',
                                           'attr_path': 'Branches',
                                           'chain_id': 7290696200003,
                                           'attrs': {'store': 'Branch',
                                                     'store_id': 'StoreID',
                                                     'store_name': 'StoreName',
                                                     'address': 'Address',
                                                     'city': 'City'}
                                           }
                               }

from routing import *

if __name__ == '__main__':
    app.run(debug=True)
