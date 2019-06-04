
from base64 import b64encode
import csv
from datetime import timedelta, datetime
from flask import jsonify, Blueprint, current_app, request
from io import StringIO
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment
from ..models import TimeLog, User

time_resolution = 60

max_delta = timedelta(minutes=15)

report_blueprint = Blueprint('report', __name__, url_prefix='/report')


csv_fields = ["user", "period", "total_time"]


def get_report_period(delta='week', start=None, stop=None):
    today = datetime.today().date()
    weekday = today.weekday()
    data = {}
    if start or stop:
        if start:
            data['start'] = start
            data['formatted'] = f"{start}"
        else:
            data['formatted'] = f"until"
        if stop:
            data['stop'] = stop
            data['formatted'] += f" {stop}"
        return data
    if delta == 'week':
        # Remove 'weekday' days until today and one week
        delta_start = timedelta(days=weekday, weeks=1)
        delta_stop = timedelta(days=weekday)
        start = today - delta_start
        stop = today - delta_stop
        return {
            'start': start,
            'stop': stop,
            'formatted': f"{start} - {stop}"
        }
    if delta == 'todate':
        formatted = f"until {today}"
        return {
            'start': None,
            'stop': today + timedelta(days=1),
            'formatted': formatted,
        }


@report_blueprint.route("", methods=['GET'])
def get_report():
    data = request.get_json() or {}
    send = True
    delta = data.get('delta', 'week')
    start = data.get('start')
    stop = data.get('stop')
    send = data.get('send', send)
    period = get_report_period(delta, start, stop)
    current_app.logger.info(period)

    report_data = report(period)
    if send in [True, 'true']:
        send_report(
            report_to_csv(report_data),
            period.get('formatted')
        )
    return jsonify(report_data)


def report_to_csv(report_data):
    csv_file = StringIO()
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(report_data)
    return csv_file.getvalue()


def report(period):
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
        )
        if period:
            start = period.get('start')
            if start:
                entries = entries.filter(
                    TimeLog.time >= start,
                )
            stop = period.get('stop')
            if stop:
                entries = entries.filter(
                    TimeLog.time < stop,
                )
        entries = entries.order_by(TimeLog.time).all()
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


def send_report(report_data, dates):
    # TODO: send message
    email_from = os.environ.get('FROM_EMAIL'))
    email_to = os.environ.get('TO_EMAIL'))
    message = Mail(
        from_email=email_from,
        to_emails=email_to,
        subject=f'Attendance report for {dates}',
        plain_text_content=f'here is the attendance report for the period of {dates}'
    )
    att = Attachment(
        b64encode(report_data.encode('utf-8')).decode(),
        # TODO: compute file name
        'blob.csv'
    )
    message.add_attachment(att)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        current_app.logger.info(response.status_code)
        current_app.logger.info(response.body)
        current_app.logger.info(response.headers)
    except Exception as e:
        current_app.logger.info(e)
