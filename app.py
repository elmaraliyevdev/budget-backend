import os
import secrets
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from routes import load_routes


def start_app():
    app = Flask(__name__)

    # ma = Marshmallow(app)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5432/postgres'
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    jwt = JWTManager(app)

    app.url_map.strict_slashes = False

    from lib.db_lib import db, ma
    db.init_app(app)
    ma.init_app(app)

    migrate = Migrate(app, db, compare_type=True)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    load_routes(app)

    return app, jwt, db


app, jwt, db = start_app()


# Populates the current_user variable provided by JWT lib with user id from JWT
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    user_id = jwt_data["sub"]
    return user_id


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True)

