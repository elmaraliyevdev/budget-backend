from typing import Dict, Tuple
from flask import abort, jsonify
from lib import db_lib
from user.model import UserSchema, UserModel
from passlib.apps import custom_app_context as pwd_context
from marshmallow.exceptions import ValidationError
from util import update_object_helper
from user.model import UserModel


def hash_password(password: str):
    return pwd_context.hash(password)


def generate_token(user: UserModel, status: int):
    user_obj = UserSchema().dump(user)
    token = user.encode_auth_token(user_obj)
    return {'user': user_obj, 'token': token}, status


def create_user(data: Dict) -> Tuple:
    if not data:
        abort(400, description="No data passed in JSON body")

    password = data.get('password').encode('utf-8')
    data['password'] = hash_password(password)
    user = UserModel.query.filter_by(email=data['email']).first()

    if user:
        return jsonify({"message": f'An account with the email {user.email} already exists.'}), 200

    try:
        user = UserSchema().load(data)
    except ValidationError as err:
        abort(400, description=err.messages)

    db_lib.insert(user)
    return generate_token(user, 201)


def login(email: str, password: str) -> Tuple:
    user = UserModel.query.filter_by(email=email).first()

    if user:

        user.check_password(password)

    else:
        abort(401, description='Invalid email or password')

    return generate_token(user, 200)


def get_user(id: int) -> Dict:
    user = UserModel.query.get_or_404(id)
    return UserSchema().dump(user)


def update_user(id: int, data: Dict) -> Tuple:
    user = UserModel.query.get_or_404(id)
    update_object_helper.is_request_valid(user, data)

    update_object_helper.update_instance(user, data)
    db_lib.commit()
    return generate_token(user, 200)


def delete_user(id: int) -> None:
    user = UserModel.query.get_or_404(id)
    db_lib.delete(user)
