from collections import defaultdict
from datetime import timedelta
from ..models import TimeLog, User

max_delta = timedelta(minutes=15)


def report(delta='1w'):
    users = User.query.all()
    report = {}
    for user in users:
        entries = TimeLog.query.filter(
            TimeLog.user == user
            # TODO: filter by delta
        ).order_by(TimeLog.time).all()
        daily_report = defaultdict({}, float)
        if entries:
            prev = entries[0]
            for entry in entries:
                date = entry.time.date
                if (
                        date == prev.time.date
                ):
                    delta = (entry.time - prev.time)
                    if delta < max_delta:
                        daily_report[date] += delta
        report[user] = daily_report
    return report
    # pull data, grouped by day+user?
    # loop over data


# pull data by user
# for each timelog group by 15 minutes slices

# db.session.query(
#  sa.func.date_trunc("day", TimeLog.time),
#  TimeLog.user).group_by(
#    sa.func.date_trunc("day", TimeLog.time), TimeLog.user).all()
# TODO: add lastseen to user


# FIXME: how to compute deltas ?
# how does the log know if the computer disappeared since
# last_seen, or if the check period is longer ?
# right now :
