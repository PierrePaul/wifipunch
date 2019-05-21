from .extensions import db


class MacAddress(db.Model):
    __tablename__ = 'macaddress'
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(
        db.String(),
        unique=True,
    )
    # Many to one
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )
    user = db.relationship(
        'User',
        back_populates="mac_addresses"
    )
