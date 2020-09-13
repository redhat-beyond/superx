from sqlalchemy import Integer, Column, Text, column, Boolean

from app import db


class Chain(db.Model):
    __tablename__ = 'chain'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)


class Branch(db.Model):
    __tablename__ = 'branch'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    chain_id = Column(db.ForeignKey('chain.id'))


class Product(db.Model):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    quantity = Column(Integer)
    is_weighted = Column(Boolean)