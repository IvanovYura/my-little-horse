import os
from importlib import import_module


def env(name: str, default: str = None):
    """
    Returns env variable value or default.
    If not set up, or no default, raise an exception to stop code evaluation.
    """
    if name not in os.environ and not default:
        raise RuntimeError(f'{name} variable is not set')

    return os.environ.get(name, default)


class Config:
    """
    For typing purposes: to avoid evaluate class attributes during import
    """

    @staticmethod
    def create(config_name: str = 'service.config.BaseConfig'):
        module_names, class_name = config_name.rsplit('.', 1)
        try:
            module = import_module(module_names)
            instance = getattr(module, class_name)
            return instance()

        except (AttributeError, TypeError, ValueError, ModuleNotFoundError) as e:
            raise ValueError(f'The config "{config_name}" is invalid: {str(e)}')


class BaseConfig(Config):
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
