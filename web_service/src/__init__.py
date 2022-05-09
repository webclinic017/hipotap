from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "secret-key-goes-here"

    # blueprint for auth routes in our app
    from .blue_prints.auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .blue_prints.main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .blue_prints.offers import offers as offers_blueprint

    app.register_blueprint(offers_blueprint)

    from .blue_prints.orders import orders as orders_blueprint
    app.register_blueprint(orders_blueprint)

    return app
