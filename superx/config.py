import os


class BaseConfig:
    # the second argument is default DBURI and can be removed
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI",
                                             "mysql+pymysql://Yet43xfTxy:HPt04GGcvA@remotemysql.com/Yet43xfTxy")

