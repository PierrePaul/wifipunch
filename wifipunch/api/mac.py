from flask import jsonify, Blueprint, request
from flask_restful import marshal
from ..utils.discover import get_local_ip, scan
from .marshal import logs_fields
from ..models import MacAddress, TimeLog
from ..models.extensions import db

mac = Blueprint('mac', __name__, url_prefix='/mac')
local_ip = get_local_ip()
ip_range = local_ip[0:local_ip.rfind('.')] + '.0/24'


@mac.route("/mine", methods=['GET'])
def get_my_mac():
    """
    """
    ip = "none"
    data = request.get_json()
    mac = False
    user = False
    if data:
        mac = data.get('mac_address')
    if not mac:
        ip = request.remote_addr
        ip_range = ip + '/32'
        scan_result = scan(ip_range)
        if len(scan_result):
            mac = scan_result[0]['mac']
    if mac:
        mac_address = MacAddress.find_one(mac)
        if mac_address and mac_address.user:
            user = mac_address.user.name
    return jsonify(
        {
            'mac': mac,
            'user': user,
            'ip': ip,
        }
    )


@mac.route("", methods=['GET'])
def list_macs():
    """
    Currently connected MAC addresses
    """
    scan_result = scan(ip_range)
    return jsonify(scan_result)


@mac.route("/log", methods=['POST'])
def write_log():
    scan_result = scan(ip_range)
    logs = []
    for result in scan_result:
        mac = result['mac']
        mac_address = MacAddress.find_one(mac)
        db.session.add(mac_address)
        user = mac_address.user
        if user:
            user = user.name
        log = TimeLog(
            mac_address=mac_address.mac_address,
            ip=result['ip'],
            user=user
        )
        db.session.add(log)
        logs += [log]
    db.session.commit()
    return jsonify(
        marshal(
            logs,
            logs_fields,
        )
    )


@mac.route("/log", methods=['GET'])
def log():
    """
    List logs, call logging function before
    """
    logs = TimeLog.query.all()
    return jsonify(marshal(logs, logs_fields))
