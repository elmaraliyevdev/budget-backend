from lib.db_lib import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy.orm.session import Session
from category.model import CategorySchema


class TransactionModel(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', lazy=True, foreign_keys=[category_id])
    date_created = db.Column(db.Date, nullable=True)
    amount = db.Column(db.Float(precision=2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), index=True,
                        nullable=False)


class TransactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TransactionModel
        load_instance = True
        include_fk = True
        sqla_session = Session

    # category = fields.Pluck(CategorySchema, 'name')
    category = fields.Nested(CategorySchema, only=['name', 'color'])
