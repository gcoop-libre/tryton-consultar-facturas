# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import os
import logging
import uuid
from logging.handlers import RotatingFileHandler


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = uuid.uuid4().hex
    LOGGING_FORMAT = "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
    LOGGING_LOCATION = 'consulta.log'
    LOGGING_LEVEL = logging.DEBUG
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', \
'application/json', 'application/javascript']
    COMPRESS_LEVEL = 8
    COMPRESS_MIN_SIZE = 500
    BOOTSTRAP_SERVE_LOCAL = True
    TRYTON_DATABASE = ''
    TRYTON_CONFIG = ''
    TRYTON_USER = '1'
    CAPTCHA_ENABLE = True
    CAPTCHA_LENGTH = 5
    CAPTCHA_WIDTH = 160
    CAPTCHA_HEIGHT = 60

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SECRET_KEY = uuid.uuid4().hex
    TRYTON_DATABASE = ''


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SECRET_KEY = uuid.uuid4().hex

config = {
    "development": "consulta.config.DevelopmentConfig",
    "testing": "consulta.config.TestingConfig",
    "default": "consulta.config.DevelopmentConfig"
}

def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
    # Configure logging
    handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], \
        maxBytes=10000000, backupCount=5)
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
