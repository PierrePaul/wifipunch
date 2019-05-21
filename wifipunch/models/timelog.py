from .extensions import db
from datetime import datetime


class TimeLog(db.Model):
    __tablename__ = 'timelog'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(
        db.DateTime,
        default=datetime.now
    )
    # NOTE: fields are strings, as we probably want to keep
    #  the data even if a user or mac disappears
    mac_address = db.Column(
        db.String(),
    )
    user = db.Column(
        db.String(),
    )
    ip = db.Column(db.String())
