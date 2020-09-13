import os


class BaseConfig:
    # the second argument is default DBURI and can be removed
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI",
                                             "mysql+pymysql://d5OJkYqkNz:3Z505SacGZ@remotemysql.com/d5OJkYqkNz")

