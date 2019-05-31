from flask import Blueprint, request, jsonify
from flask_restful import marshal

from .marshal import user_fields
from ..models import User
from ..models.extensions import db
user = Blueprint('user', __name__, url_prefix='/user')


@user.route(
    "",
    methods=['GET']
)
@user.route(
    "/<username>",
    methods=['GET']
)
def list_users(username=False):
    """
    """
    users = User.query
    if username:
        users = users.filter(User.name == username)
    users = users.all()
    return jsonify(marshal(users, user_fields))


@user.route("", methods=['POST'])
def create_user():
    """
    """
    data = request.get_json()
    username = data.get('username')
    user = User.get_or_create(
        username=username
    )
    return jsonify(marshal(user, user_fields))
