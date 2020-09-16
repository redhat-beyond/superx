from sqlalchemy import Integer, Column, Text, Boolean, Float

from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    password = Column(Text)


class Chain(db.Model):
    __tablename__ = 'chain'

    id = Column(Integer, primary_key=True)
    name = Column(Text)


class Branch(db.Model):
    __tablename__ = 'branch'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    address = Column(Text)
    sub_chin_id = Column(Integer)
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

    item_code = Column(db.ForeignKey('product.id'), primary_key=True)
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
