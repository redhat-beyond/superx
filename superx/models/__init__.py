from sqlalchemy import Integer, Column, Text, Boolean, Float
from flask_login import LoginManager, UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(15))
    email = Column(db.String(50), unique=True)
    password = Column(db.String(80))

class Chain(db.Model):
    __tablename__ = 'chain'

    id = Column(Integer, primary_key=True)
    name = Column(Text)


class Branch(db.Model):
    __tablename__ = 'branch'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    address = Column(Text)
    sub_chain_id = Column(Integer)
    chain_id = Column(db.ForeignKey('chain.id'))


class Product(db.Model):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    quantity = Column(Integer)
    is_weighted = Column(Boolean)
    unit_of_measure = Column(Text)


class BranchPrice(db.Model):
    __tablename__ = 'branch_price'

    branch_price_id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(db.ForeignKey('product.id'))
    branch_id = Column(db.ForeignKey('branch.id'))
    price = Column(Integer)
    update_date = Column(Text)


class Basket(db.Model):
    __tablename__ = 'basket'

    id = Column(Integer, primary_key=True)
    cheapest_branch_id = Column(db.ForeignKey('branch.id'))
    user_id = Column(db.ForeignKey('user.id'))

    items = db.relationship('BasketProduct', primaryjoin='Basket.id == BasketProduct.basket_id')


class BasketProduct(db.Model):
    __tablename__ = 'basket_product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    basket_id = Column(db.ForeignKey('basket.id'))
    product_id = Column(db.ForeignKey('product.id'))

    product = db.relationship('Product', primaryjoin='BasketProduct.product_id == Product.id', uselist=False)
    basket = db.relationship('Basket', primaryjoin='BasketProduct.basket_id == Basket.id', uselist=False)

