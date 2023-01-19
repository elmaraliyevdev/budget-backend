from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm.session import Session
from marshmallow import fields
from datetime import datetime
from lib.db_lib import db
import jwt
import os
from passlib.apps import custom_app_context as pwd_context
from flask import abort
from wallet.model import WalletSchema


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(280), nullable=False)
    date_created = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    admin = db.Column(db.Boolean, default=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'))
    wallet = db.relationship("WalletModel", backref="user", lazy=True, foreign_keys=[wallet_id])

    def encode_auth_token(self, user):
        try:
            payload = {
                'iat': datetime.utcnow(),
                'iss': 'portal',
                'sub': user
            }
            return jwt.encode(
                payload,
                os.getenv('JWT_SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def check_password(self, password):
        valid = pwd_context.verify(password, self.password)
        if not valid:
            abort(401, "Invalid email or password.")


class UserSchema(SQLAlchemyAutoSchema):
    password = fields.Str(load_only=True)

    class Meta:
        model = UserModel
        load_instance = True
        include_fk = True
        sqla_session = Session

    wallet = fields.Nested(WalletSchema(only=("id", "name", "currency", "balance", "created_date")))
