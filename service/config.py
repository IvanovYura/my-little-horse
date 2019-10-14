import os


class BaseConfig:
    SERVICE_NAME = 'graph_ql'

    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 54320))
    DB_NAME = os.environ.get('DB_NAME', SERVICE_NAME)
    DB_USER = os.environ.get('DB_USER', SERVICE_NAME)
    DB_PASSWORD = os.environ.get('DB_PASSWORD', SERVICE_NAME)

    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
