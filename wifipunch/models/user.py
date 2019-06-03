from .extensions import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    mac_addresses = db.relationship(
        "MacAddress",
        back_populates="user"
    )

    @classmethod
    def get_or_create(cls, *args, **kwargs):
        username = kwargs.get('username')
        user = False
        if username:
            user = User.query.filter(
                User.name == username
            ).first()
        if not user:
            user = cls(**kwargs)
            db.session.add(user)
            db.session.commit()
        return user
