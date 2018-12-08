from flask import Flask
from flask_cors import CORS

from web_api import auth, api
from web_api.extensions import db, jwt, migrate


def create_app(config=None, testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask('data_api')
    CORS(app)

    configure_app(app, testing)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    configure_extensions(app, cli)
    register_blueprints(app)

    return app


def configure_app(app, testing=False):
    """set configuration for application
    """
    # default configuration
    app.config.from_object('web_api.config')

    if testing is True:
        # override with testing config
        app.config.from_object('web_api.configtest')
    else:
        # override with env variable, fail silently if not set
        app.config.from_envvar("DATA_API_CONFIG", silent=True)


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
