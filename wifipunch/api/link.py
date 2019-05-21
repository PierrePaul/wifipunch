from flask import request, jsonify, Blueprint
from flask_restful import marshal

from .marshal import mac_fields
from ..models import MacAddress, User
from ..models.extensions import db

link = Blueprint('link', __name__, url_prefix='/link')


@link.route("", methods=['GET'])
def list_links():
    """
    """
    macs = MacAddress.query.all()
    return jsonify(marshal(macs, mac_fields))


@link.route("", methods=['POST'])
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
