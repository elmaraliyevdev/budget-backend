from category.model import CategoryModel, CategorySchema
from typing import List, Dict
from lib import db_lib
from flask import abort
from marshmallow.exceptions import ValidationError
from util import update_object_helper


def get_categories(user_id: int) -> List[Dict]:
    categories = CategoryModel.query.filter_by(user_id=user_id).all()

    # for category in categories:
    #     for transaction in category.transactions:
    #         print("transaction", transaction.name)

    return CategorySchema(many=True).dump(categories)


def add_category(data: Dict, user_id: int) -> int:
    data['user_id'] = user_id

    if not data:
        abort(400, description="No data passed in JSON body")
    try:
        category = CategorySchema().load(data)
    except ValidationError as err:
        abort(400, description=err.messages)
    return db_lib.insert(category)


def get_category(id: int) -> Dict:
    category = CategoryModel.query.get_or_404(id)

    return CategorySchema().dump(category)


def update_category(id: int, data: Dict) -> None:
    print("data", data)
    category = CategoryModel.query.get_or_404(id)
    update_object_helper.is_request_valid(category, data)
    update_object_helper.update_instance(category, data)
    db_lib.commit()


def delete_category(id: int) -> None:
    category = CategoryModel.query.get_or_404(id)
    db_lib.delete(category)
