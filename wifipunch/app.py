#!/bin/env python3
from .discover import get_local_ip, scan
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, fields, marshal_with, marshal

app = Flask(__name__)
app.config['DATABASE_URL'] = "postgresql://wifipunch@db/wifipunch"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://wifipunch@db/wifipunch"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

local_ip = get_local_ip()
ip_range = local_ip[0:local_ip.rfind('.')] + '.0/24'


class MacAddress(db.Model):
    __tablename__ = 'macaddress'
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(
        db.String(),
        unique=True,
    )


class TimeLog(db.Model):
    __tablename__ = 'timelog'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    # One to Many (macaddress)
    mac_addresses_id = db.Column(
        db.Integer,
        db.ForeignKey('macaddress.id')
    )
    mac_addresses = db.relationship(
        'MacAddress',
        backref=db.backref('users', lazy=True)
    )


mac_fields = {
    'mac_address': fields.String(
        attribute='mac'
    ),
}

user_fields = {
    'name': fields.String,
    'mac_addresses': fields.List(
        fields.Nested(mac_fields)
    ),
}
user_list_fields = {
    fields.List(
        fields.Nested(user_fields)
    ),
}


# @marshal_with(
#     user_fields,
# )
@app.route("/user", methods=['GET'])
def list_users():
    """
    """
    users = User.query.all()
    return jsonify(marshal(users, user_fields))


# @app.route("/user", methods=['POST'])
# @marshal_with(
#     user_fields,
# )
@app.route("/user/<username>", methods=['get'])
def create_user(username):
    """
    """
    # TODO: POST + request.get_json()
    user = User.query.filter(
        User.name == username
    ).all()
    if not user:
        user = User(
            name=username
        )
        db.session.add(user)
        db.session.commit()
        # return user.name
    return jsonify(marshal(user, user_fields))


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
