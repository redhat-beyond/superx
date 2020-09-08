"""Data models."""
from . import db


class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'item_info'
    item_code = db.Column(
        db.Integer,
        primary_key=True
        nullable = False;
    )
    item_name = db.Column(
        db.String,
        nullable = False;
    )
    item_unit_of_measure= db.Column(
        db.String,
        nullable = False;
    )
    item_unit_of_measure_qty= db.Column(
        db.Integer,
        nullable = False;
    )

    __tablename__ = 'item_prices'
    item_code = db.Column(
        db.Integer,
        primary_key=True
        nullable = False;
    )
    item_price_shufersal = db.Column(
        db.Integer,
        nullable = False;
    )
    item_price_mega = db.Column(
        db.Integer,
        nullable = False;
    )
    
    def __repr__(self):
        return '<Item {}>'.format(self.item_name)