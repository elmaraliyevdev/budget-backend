from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, current_user
from wallet import controller

wallet_api = Blueprint("wallets", __name__)


@wallet_api.route("/", methods=["GET", "POST"])
@jwt_required()
def get_wallets():
    if request.method == "GET":
        wallets = controller.get_wallets(current_user["id"])

        return jsonify(wallets)

    elif request.method == "POST":
        data = request.get_json()

        print("data", data)

        id = controller.add_wallet(data, current_user["id"])
        print("id", id)
        return {"id": id}, 201


@wallet_api.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def get_transaction(id: int):
    if request.method == "GET":
        wallet = controller.get_wallet(id)

        return wallet

    elif request.method == "PUT":
        data = request.get_json()
        controller.update_wallet(id, data)
        return {"success": True}

    elif request.method == "DELETE":
        controller.delete_wallet(id)
        return {"success": True}