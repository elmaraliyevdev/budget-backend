api_prefix = '/api/v1'


def load_routes(app):
    from user.routes import user_api
    from category.routes import category_api
    from transaction.routes import transaction_api
    from wallet.routes import wallet_api

    app.register_blueprint(user_api, url_prefix=f"{api_prefix}/register", name="signup")
    app.register_blueprint(user_api, url_prefix=f"{api_prefix}")
    app.register_blueprint(category_api, url_prefix=f"{api_prefix}/categories")
    app.register_blueprint(transaction_api, url_prefix=f"{api_prefix}/transactions")
    app.register_blueprint(wallet_api, url_prefix=f"{api_prefix}/wallets")
