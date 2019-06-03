import csv
from datetime import timedelta
from flask import jsonify, Blueprint, current_app
from io import StringIO
from ..models import TimeLog, User

time_resolution = 60

max_delta = timedelta(minutes=15)

report_blueprint = Blueprint('report', __name__, url_prefix='/report')


csv_fields = ["user", "period", "total_time"]


@report_blueprint.route("", methods=['GET'])
def get_report():
    return jsonify(report())


def report_to_csv():
    rep = report()
    csv_file = StringIO()
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(rep)
    return csv_file.getvalue()


def report(delta='1w'):
    """
    Generate a report for each user, grouped by dates
    If two 'checkins' are too far appart (max_delta), the user is
    considered as logged out between those two times.
    If two checkins are of different dates, one will be
    a checkout, the other is a checkin for the next day
    """
    users = User.query.all()
    report_file = []
    for user in users:
        entries = TimeLog.query.filter(
            TimeLog.user == user.name
            # TODO: filter by delta
        ).order_by(TimeLog.time).all()
        if entries:
            (entries)
            prev = entries[0]
            last = entries[-1]
            total = 0.0
            for entry in entries:
                date = entry.time.date()
                date_changed = (date != prev.time.date())
                if not (date_changed):
                    delta = (entry.time - prev.time)
                    if delta < max_delta:
                        total += delta.total_seconds()/time_resolution
                if entry == last or date_changed:
                    report_file.append([
                            user.name,
                            prev.time.date().isoformat(),
                            total
                    ])
                prev = entry
    return report_file
