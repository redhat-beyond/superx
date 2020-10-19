'''
import os
'''
import os


class BaseConfig: #pylint: disable=too-few-public-methods
    '''
    configuring database to attach to remote SQL
    '''
    # the second argument is default DBURI and can be removed
    SQLALCHEMY_DATABASE_URI = os.environ.get("""SQLALCHEMY_DATABASE_URI",
                    "mysql+pymysql://
                    Super_User:SuperX1234@mysql-13101-0.cloudclusters.net:13101/SuperX""")
