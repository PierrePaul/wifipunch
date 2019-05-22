from flask import request, jsonify, Blueprint
from flask_restful import marshal

from .marshal import mac_fields
from ..models import MacAddress, User
from ..models.extensions import db
from ..utils.discover import scan

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
    mac = False
    data = request.get_json()
    if data:
        mac = data.get('mac_address')
    if not mac:
        ip = request.remote_addr
        scan_result = scan(ip)
        if len(scan_result):
            mac = scan_result[0]['mac']
    username = data.get('username')
    mac_address = MacAddress.find_one(mac)
    user = User.query.filter(
        User.name == username
    ).first()
    if user:
        mac_address.user = user
        db.session.add(mac_address)
        db.session.commit()
        return jsonify(marshal(mac_address, mac_fields))
    return jsonify({})
