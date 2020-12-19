from flask import session, request

from app.extends.error import HttpError


def check_login():
    if request.endpoint not in ['session.login', 'users.create_user'] and request.method != 'OPTIONS':
        if 'uuid' not in session:
            raise HttpError(401, '请先登录')
