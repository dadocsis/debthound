"""Default configuration

Use env var to override
"""
import os
from configparser import ConfigParser

file = os.path.abspath(os.path.join(os.path.join(__file__, '../..'), 'secrets.ini'))
secrets = ConfigParser()
secrets.read(file)

DEBUG = True
ENV = os.environ.get('ENV', 'prod')
SECRET_KEY = secrets.get(ENV, 'sk')
ADMIN_PW = secrets.get(ENV, 'admin_pw')

SQLALCHEMY_DATABASE_URI = secrets.get(ENV, 'db_uri')
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
JWT_ACCESS_TOKEN_EXPIRES = False
