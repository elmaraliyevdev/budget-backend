from lib.db_lib import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm.session import Session
from datetime import datetime


class WalletModel(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    currency = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Float(precision=2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


class WalletSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WalletModel
        load_instance = True
        include_relationships = True
        include_fk = True
        sqla_session = Session
