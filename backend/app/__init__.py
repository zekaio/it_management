import os

import click
from flask import Flask, jsonify
from flask.json import JSONEncoder
import datetime

from app.config import app_config
from app.controllers import *
from app.extends.error import HttpError
from app.extensions import db, migrate, cors
from app.middlewares import before_request
from app.models.database import *


def create_app(config_name: str = None) -> Flask:
    """
    :param config_name: str in ['development', 'production', 'testing']
    :return: Flask app
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    register_errorhandler(app)
    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    register_middleware(app)
    register_json_encoder(app)

    return app


def register_errorhandler(app: Flask):
    @app.errorhandler(HttpError)
    def handle_http_error(error: HttpError):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response


def register_blueprints(app: Flask):
    app.register_blueprint(users_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(comments_bp)


def register_extensions(app: Flask):
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)


def register_middleware(app: Flask):
    app.before_request(before_request)


def register_json_encoder(app: Flask):
    class CustomJSONEncoder(JSONEncoder):
        def default(self, obj):
            try:
                if isinstance(obj, datetime.datetime):
                    return obj.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(obj, datetime.date):
                    return obj.strftime('%Y-%m-%d')
                iterable = iter(obj)
            except TypeError:
                pass
            else:
                return list(iterable)
            return JSONEncoder.default(self, obj)

    app.json_encoder = CustomJSONEncoder


def register_commands(app: Flask):
    @app.cli.command()
    def initdb():
        """
        初始化数据库
        """
        db.create_all()
        db.session.commit()
        click.echo('Initialized database.')

    @app.cli.command()
    def dropdb():
        """
        清空数据表
        """
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
        db.create_all()
        db.session.commit()
        click.echo('Initialized database.')

    @app.cli.command()
    def forge():
        """
        向数据库中插入模拟数据
        """
        pass
