#!/bin/env python3
from .discover import get_local_ip, scan
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DATABASE_URL'] = "postgresql://db/wifipunch"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://db/wifipunch"
db = SQLAlchemy(app)

local_ip = get_local_ip()
ip_range = local_ip[0:local_ip.rfind('.')] + '.0/24'


class MacAddress(db.Model):
    __tablename__ = 'macaddress'
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String())
    # TODO: o2m(timelog)


class TimeLog(db.Model):
    __tablename__ = 'timelog'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    # TODO: m2m(macaddress)


@app.route("/user", methods=['GET'])
def list_users():
    """
    """
    users = []
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
