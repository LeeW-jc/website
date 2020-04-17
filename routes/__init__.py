from flask import session
from models.user import User


def current_user():
    u_id = session.get('user_id', -1)
    u = User.find_by(id=u_id)
    return u
