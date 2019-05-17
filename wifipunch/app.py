#!/bin/env python3
from .discover import get_local_ip, scan
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, fields, marshal_with

app = Flask(__name__)
app.config['DATABASE_URL'] = "postgresql://db/wifipunch"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://db/wifipunch"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

local_ip = get_local_ip()
ip_range = local_ip[0:local_ip.rfind('.')] + '.0/24'


class MacAddress(db.Model):
    __tablename__ = 'macaddress'
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String())


class TimeLog(db.Model):
    __tablename__ = 'timelog'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    # One to Many (macaddress)
    mac_addresses_id = db.Column(
        db.Integer,
        db.ForeignKey('macaddress.id')
    )
    mac_addresses = db.relationship(
        'MacAddress',
        backref=db.backref('users', lazy=True)
    )


user_fields = {
    'name': fields.String,
    'mac_addresses': fields.List(
        fields.String(attribute='mac'),
    )
}


@marshal_with(
    user_fields,
    envelope='resource'
)
@app.route("/user", methods=['GET'])
def list_users():
    """
    """
    users = User.query.all()
    return users


@app.route("/user", methods=['POST'])
def create_user():
    """
    """
    users = []
    return users


@app.route("/link", methods=['GET'])
def list_links():
    """
    """
    links = []
    return links


@app.route("/link", methods=['POST'])
def create_link():
    """
    """
    links = []
    return links


@app.route("/mac", methods=['GET'])
def list_macs():
    """
    Currently connected MAC addresses
    """
    print("blah")
    scan_result = scan(ip_range)
    return jsonify(scan_result)
