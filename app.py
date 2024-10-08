import os

from flask import Flask
from flask_migrate import Migrate

from heart.core.extensions import db
from heart.core.seeder import seed_categories, seed_severities, seed_tickets
from routes.public import routes as publicRoutes
from utils.apiMessages import LocalApiCode, error_message


def _notFound(error):
    return {"errors": [error_message(LocalApiCode.unknownRoute)]}, 404


def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")
    if env == "development":
        app.config.from_object("config.DevelopmentConfig")
    elif env == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.ProductionConfig")

    db.init_app(app)

    Migrate(app, db)

    for route in publicRoutes:
        app.add_url_rule(
            rule=route.path,
            view_func=route.handler.as_view(route.name),
            methods=route.methods,
        )
    app.register_error_handler(404, _notFound)

    with app.app_context():
        db.create_all()
        seed_severities()
        seed_categories()
        seed_tickets()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True)
