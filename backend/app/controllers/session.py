from flask import Blueprint, session

from app.models.controller import UserModel
from app.services import database
from app.extends.result import Result

session_bp = Blueprint('session', __name__, url_prefix='/session')


@session_bp.route('', methods=['POST'])
def login():
    """
    用户登录
    :param: username: 用户名
    :param: password: 密码
    :return: {
        "data": {
            "uuid": "uuid",
            "username":"用户名"
        },
        "msg": "OK",
        "status": 200
    }
    """
    user: UserModel = UserModel.get_parameters()

    uuid, username = database.user_login(user.username, user.password)
    session['uuid'] = uuid
    return Result.OK().data({
        'uuid': uuid,
        'username': username
    }).build()


@session_bp.route('', methods=['DELETE'])
def logout():
    """
    退出登录
    :return: {
        "data": null,
        "msg": "OK",
        "status": 200
    }
    """
    if session.get('uuid'):
        session['uuid'] = None

    return Result.OK().build()
