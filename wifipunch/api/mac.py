import socket
import os
from datetime import datetime
from flask import jsonify, Blueprint, request, abort
from flask_restful import marshal
from ..utils.discover import get_local_ip, scan, get_hostname
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
            'hostname': get_hostname(ip),
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
    api_key = os.environ.get('WIFIPUNCH_API_KEY')
    data = request.get_json() or {}
    key = data.get('api_key')
    if not key or api_key != key:
        abort(403, "Operation not permitted.")

    scan_result = scan(ip_range)
    logs = []
    time = datetime.now()
    for result in scan_result:
        mac = result['mac']
        mac_address = MacAddress.find_one(mac)
        db.session.add(mac_address)
        db_user = mac_address.user
        if db_user:
            user = db_user.name
            db_user.last_seen = time
        else:
            user = "Unknown User"
        log = TimeLog(
            mac_address=mac_address.mac_address,
            ip=result['ip'],
            user=user,
            time=time,
            hostname=get_hostname(result['ip'])
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
