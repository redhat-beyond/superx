# '''
# import os
# '''
# import os
# from dataclasses import dataclass

# @dataclass
# class BaseConfig:
#     '''
#     configuring database to remote mySQL database
#     '''
#     SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI",         #pylint: disable=wrong-import-position
#         "mysql+pymysql://Super_User:SuperX1234@mysql-13101-0.cloudclusters.net:13101/SuperX")
