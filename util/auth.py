from flask import abort
from user.model import UserModel
from typing import Dict


def authorised_admin(user: Dict):
    user = UserModel.query.get_or_404(user['id'])

    if not user.admin:
        abort(404)


def authorised_user(obj_user_id: int, user_id: int):
    if not obj_user_id == user_id:
        abort(404)
