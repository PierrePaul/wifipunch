#!/bin/env python3
from flask import Flask, send_file, send_from_directory
from flask_migrate import Migrate
from flask_cors import CORS
from .models.extensions import db
from .api import (
    mac_blueprint,
    user_blueprint,
    link_blueprint,
    report_blueprint
)


def create_app(config=None):
    app = Flask(__name__)
    CORS(app)
    app.config[
        'SQLALCHEMY_DATABASE_URI'
    ] = "postgresql://wifipunch@db/wifipunch"
    app.register_blueprint(mac_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(link_blueprint)
    app.register_blueprint(report_blueprint)
    db.init_app(app)
    Migrate(app, db)
    return app


app = create_app()


@app.route('/')
def root():
    return send_file('/frontend/index.html')


@app.route('/_nuxt/<path:path>')
def send_js(path):
    return send_from_directory('/frontend/_nuxt', path)
