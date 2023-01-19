from typing import List, Dict
from flask import abort
from marshmallow.exceptions import ValidationError
from lib import db_lib
from wallet.model import WalletModel, WalletSchema
from util import update_object_helper


def get_wallets(user_id: int) -> List[Dict]:
    wallets = WalletModel.query.filter_by(user_id=user_id).all()

    return WalletSchema(many=True).dump(wallets)


def get_wallet(id: int) -> Dict:
    wallet = WalletModel.query.get_or_404(id)

    return WalletSchema().dump(wallet)


def add_wallet(data: Dict, user_id: int) -> int:
    if not data:
        abort(400, description="No data passed in JSON body")
    try:
        data["user_id"] = user_id
        wallet = WalletSchema().load(data)
        print("wallet", wallet)
    except ValidationError as err:
        abort(400, description=err.messages)
    return db_lib.insert(wallet)


def update_wallet(id: int, data: Dict) -> None:
    wallet = WalletModel.query.get_or_404(id)
    update_object_helper.is_request_valid(wallet, data)
    update_object_helper.update_instance(wallet, data)
    db_lib.commit()


def delete_wallet(id: int) -> None:
    wallet = WalletModel.query.get_or_404(id)
    db_lib.delete(wallet)
