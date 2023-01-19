from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from category import controller

category_api = Blueprint('categories', __name__)


@category_api.route('/', methods=['GET', 'POST'])
@jwt_required()
def get_categories():
    if request.method == "GET":
        categories = controller.get_categories(user_id=current_user["id"])

        return categories, 200

    elif request.method == "POST":
        data = request.get_json()
        print("data", data)
        category = controller.add_category(data=data, user_id=current_user["id"])

        return {'category': category}, 201


@category_api.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def get_category(id: int):
    if request.method == "GET":
        category = controller.get_category(id)

        return category

    elif request.method == "PUT":
        data = request.get_json()
        print("data", data)
        controller.update_category(id, data)
        return {"success": True}

    elif request.method == "DELETE":
        controller.delete_category(id)
        return {"success": True}

