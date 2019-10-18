import os


class BaseConfig:
    SERVICE_NAME = 'graph_ql'

    ADMIN_USER = 'admin'
    ADMIN_PASSWORD = 'admin'

    BASIC_AUTH_FORCE = True

    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 54320))
    DB_NAME = os.environ.get('DB_NAME', SERVICE_NAME)
    DB_USER = os.environ.get('DB_USER', SERVICE_NAME)
    DB_PASSWORD = os.environ.get('DB_PASSWORD', SERVICE_NAME)

    DB_ADMIN_USER = os.environ.get('DB_ADMIN_USER', 'postgres')
    DB_ADMIN_PASSWORD = os.environ.get('DB_ADMIN_PASSWORD', 'postgres')

    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    DB_NAME = os.environ.get('DB_NAME', f'test_{BaseConfig.SERVICE_NAME}')
    DB_USER = os.environ.get('DB_USER', f'test_{BaseConfig.SERVICE_NAME}')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', f'test_{BaseConfig.SERVICE_NAME}')
