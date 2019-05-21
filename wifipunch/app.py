#!/bin/env python3
from .discover import get_local_ip, scan
from datetime import datetime
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
    mac_address = db.Column(
        db.String(),
        unique=True,
    )
    # Many to one
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )
    user = db.relationship(
        'User',
        back_populates="mac_addresses"
    )


class TimeLog(db.Model):
    __tablename__ = 'timelog'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(
        db.DateTime,
        default=datetime.now
    )
    # NOTE: fields are strings, as we probably want to keep
    #  the data even if a user or mac disappears
    mac_address = db.Column(
        db.String(),
    )
    user = db.Column(
        db.String(),
    )
    ip = db.Column(db.String())


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    mac_addresses = db.relationship(
        "MacAddress",
        back_populates="user"
    )


mac_fields = {
    'mac_address': fields.String(),
    'user': fields.String(attribute='user.name')
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

logs_fields = {
    'time': fields.String,
    'mac_address': fields.String,
    'user': fields.String,
    'ip': fields.String,
}


@app.route(
    "/user",
    methods=['GET']
)
@app.route(
    "/user/<username>",
    methods=['GET']
)
def list_users(username=False):
    """
    """
    users = User.query
    if username:
        users = users.filter(User.name == username)
    users = users.all()
    return jsonify(marshal(users, user_fields))


@app.route("/user", methods=['POST'])
def create_user():
    """
    """
    data = request.get_json()
    username = data.get('username')
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
    macs = MacAddress.query.all()
    return jsonify(marshal(macs, mac_fields))


@app.route("/link", methods=['POST'])
def create_link():
    """
    """
    data = request.get_json()
    mac = data.get('mac_address')
    username = data.get('username')
    mac_address = MacAddress.query.filter(
        MacAddress.mac_address == mac
    ).first()
    if not mac_address:
        mac_address = MacAddress(mac_address=mac)
    user = User.query.filter(
        User.name == username
    ).first()
    if user:
        mac_address.user = user
        db.session.add(mac_address)
        db.session.commit()
        return jsonify(marshal(mac_address, mac_fields))
    return jsonify({})


@app.route("/mac", methods=['GET'])
def list_macs():
    """
    Currently connected MAC addresses
    """
    scan_result = scan(ip_range)
    return jsonify(scan_result)

@app.route("/log", methods=['GET'])
def log():
    """
    List logs, call logging function before
    """
    scan_result = scan(ip_range)
    for result in scan_result:
        mac = result['mac']
        mac_address = MacAddress.query.filter(
            MacAddress.mac_address == mac
        ).first()
        user = mac_address.user.name
        log = TimeLog(
            mac_address=mac_address.mac_address,
            ip=result['ip'],
            user=user
        )
        db.session.add(log)
        db.session.commit()
    logs = TimeLog.query.all()
    return jsonify(marshal(logs, logs_fields))
