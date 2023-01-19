from typing import List, Dict
from flask import abort
from marshmallow.exceptions import ValidationError
from lib import db_lib
from transaction.model import TransactionModel, TransactionSchema
from util import update_object_helper


def get_transactions(user_id: int) -> List[Dict]:
    transactions = TransactionModel.query.filter_by(user_id=user_id).order_by(TransactionModel.date_created.asc()).all()

    return TransactionSchema(many=True).dump(transactions)


def get_transaction(id: int) -> Dict:
    product = TransactionModel.query.get_or_404(id)

    return TransactionSchema().dump(product)


def add_transaction(data: Dict, user_id: int) -> int:
    if not data:
        abort(400, description="No data passed in JSON body")
    try:
        data["user_id"] = user_id
        transaction = TransactionSchema().load(data)
    except ValidationError as err:
        abort(400, description=err.messages)
    return db_lib.insert(transaction)


def get_transactions_for_category(category_id: int) -> List[TransactionModel]:
    transactions = TransactionModel.query.filter_by(category_id=category_id).all()
    transactions.sort(key=lambda x: x.name)
    return TransactionSchema(many=True).dump(transactions)


def update_transaction(id: int, data: Dict) -> None:
    transaction = TransactionModel.query.get_or_404(id)
    update_object_helper.is_request_valid(transaction, data)
    update_object_helper.update_instance(transaction, data)
    db_lib.commit()


def delete_transaction(id: int) -> None:
    transaction = TransactionModel.query.get_or_404(id)
    db_lib.delete(transaction)
