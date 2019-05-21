from flask import jsonify, Blueprint
from flask_restful import marshal
from ..utils.discover import get_local_ip, scan
from .marshal import logs_fields
from ..models import MacAddress, TimeLog
from ..models.extensions import db

mac = Blueprint('mac', __name__, url_prefix='/mac')
local_ip = get_local_ip()
ip_range = local_ip[0:local_ip.rfind('.')] + '.0/24'


@mac.route("", methods=['GET'])
def list_macs():
    """
    Currently connected MAC addresses
    """
    scan_result = scan(ip_range)
    return jsonify(scan_result)


@mac.route("/log", methods=['GET'])
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
