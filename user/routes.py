from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from user import controller
from util.auth import authorised_user

user_api = Blueprint("users", __name__)


@user_api.route("/register", methods=["POST"])
def user_register():
    data = request.get_json()
    user = controller.create_user(data)

    return user


@user_api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = controller.login(email, password)
    return user


@user_api.route("/user/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]

        return {"access_token": new_token}, 200


@user_api.route("/user/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        return {"message": "User logged out successfully."}, 200


@user_api.route("/users/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def users(id: int):
    current_user = get_jwt_identity()

    authorised_user(current_user["id"], id)

    if request.method == "GET":
        user = controller.get_user(id)
        return user

    elif request.method == "PUT":
        data = request.get_json()
        return controller.update_user(id, data)

    elif request.method == "DELETE":
        controller.delete_user(id)
        return {"success": True}


# @user_api.route("/user/<string:user_id>")
# class User(MethodView):
#     @user_api.response(200, UserSchema)
#     def get(self, user_id):
#         user = UserModel.query.get_or_404(user_id)
#         return user
#
#     def delete(self, user_id):
#         user = UserModel.query.get_or_404(user_id)
#         db.session.delete(user)
#         db.session.commit()
#
#         return {"message": "User deleted."}, 200
#
#     @user_api.arguments(UserSchema)
#     @user_api.response(200, UserSchema)
#     def put(self, data, user_id):
#         user = UserModel.query.get(user_id)
#         if user:
#             user.username = data["username"]
#             user.email = data["email"]
#             user.password = data["password"]
#         else:
#             user = UserModel(id=user_id, **data)
#
#         db.session.add(user)
#         db.session.commit()
#
#         return user
