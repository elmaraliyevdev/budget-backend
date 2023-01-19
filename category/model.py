from lib.db_lib import db
from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm.session import Session


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String)
    created_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    color = db.Column(db.String(80), unique=True, nullable=True)
    # transactions = db.relationship('TransactionModel', backref='category', lazy='dynamic')


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CategoryModel
        load_instance = True
        include_relationships = True
        include_fk = True
        sqla_session = Session
