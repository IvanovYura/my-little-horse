import os

from flask import Flask
from flask_graphql import GraphQLView

from service.schema import schema
from service.config import BaseConfig
from service.db import database


def create_app(config: BaseConfig) -> Flask:
    app = Flask(__name__)
    _assign_config(app, config)

    app.add_url_rule(
        '/',
        view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    )

    app.teardown_appcontext(close_connection)

    return app


def _assign_config(app: Flask, config: BaseConfig):
    try:
        app.config.from_object(config)
    except (ImportError, ModuleNotFoundError) as e:
        raise ValueError(f'The config "{config}" is invalid: {str(e)}')


def close_connection(exception=None):
    database.close_connection()


if __name__ == '__main__':
    config = os.environ.get('APP_SETTINGS', 'service.config.DevelopmentConfig')
    app = create_app(config)
    app.run()
