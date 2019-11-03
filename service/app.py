import os

from flask import Flask
from flask_graphql import GraphQLView

from service.authentication import init_basic_auth
from service.db.init_db import init_db
from service.schema.schema import schema
from service.config import Config
from service.db import database


def create_app(config: Config) -> Flask:
    """
    Creates Flask application with specified config
    """
    app = Flask(__name__)

    app.config.from_object(config)

    app.add_url_rule(
        '/',
        view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    )

    app.teardown_appcontext(close_connection)

    return app


def close_connection(exception=None):
    # close connection after each request
    database.close_connection()


def main():
    config_name = os.environ.get('APP_SETTINGS', 'service.config.DevelopmentConfig')
    config = Config.create(config_name)

    app = create_app(config)

    init_basic_auth(app)

    init_db()

    app.run(use_reloader=False)


if __name__ == '__main__':
    main()
