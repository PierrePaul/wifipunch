from flask import jsonify, Blueprint
from collections import defaultdict
from datetime import timedelta
from ..models import TimeLog, User

time_resolution = 60

max_delta = timedelta(minutes=15)

report_blueprint = Blueprint('report', __name__, url_prefix='/report')


@report_blueprint.route("", methods=['GET'])
def report(delta='1w'):
    users = User.query.all()
    report = {}
    for user in users:
        entries = TimeLog.query.filter(
            TimeLog.user == user.name
            # TODO: filter by delta
        ).order_by(TimeLog.time).all()
        daily_report = defaultdict(float)
        if entries:
            prev = entries[0]
            for entry in entries:
                date = entry.time.date()
                if (
                        date == prev.time.date()
                ):
                    delta = (entry.time - prev.time)
                    if delta < max_delta:
                        daily_report[
                            date.isoformat()
                        ] += delta.total_seconds()/time_resolution
                prev = entry
        report[user.name] = daily_report
    return jsonify(report)
