from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, current_user
from transaction import controller

transaction_api = Blueprint("transactions", __name__)


@transaction_api.route("/", methods=["GET", "POST"])
@jwt_required()
def get_transactions():
    if request.method == "GET":
        if "category_id" in request.args:
            category_id = request.args["category_id"]
            try:
                category_id = int(category_id)
            except ValueError as err:
                abort(400, description=f"Category ID provided was not an integer, received {category_id}")
            transactions = controller.get_transactions_for_category(category_id)
        else:
            transactions = controller.get_transactions(current_user["id"])
        return jsonify(transactions)

    elif request.method == "POST":
        data = request.get_json()
        id = controller.add_transaction(data, current_user["id"])
        return {"id": id}, 201


@transaction_api.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def get_transaction(id: int):
    if request.method == "GET":
        product = controller.get_transaction(id)

        return product

    elif request.method == "PUT":
        data = request.get_json()
        controller.update_transaction(id, data)
        return {"success": True}

    elif request.method == "DELETE":
        controller.delete_transaction(id)
        return {"success": True}