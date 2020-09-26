from flask import Blueprint, request, session

from app.models.controller import *
from app.services import database
from app.extends.result import Result
from app.extends.error import HttpError

user_bp = Blueprint('user', __name__, url_prefix='/user')


# 注册
@user_bp.route('', methods=['POST'])
def create_user():
    """
    用户注册
    :param: username: 用户名
    :param: password: 密码
    :param: check_pwd: 二次验证密码
    :return: {
        "data": null,
        "msg": "OK",
        "status": 200
    }
    """
    user: UserModel = UserModel.get_parameters()
    if user.password != user.check_pwd:
        raise HttpError(400, '两次填写的密码不一致')
    database.create_user(username=user.username, password=user.password)
    return Result.OK().build()


# 修改密码
@user_bp.route('/password', methods=['PUT'])
def update_user_password():
    """
    修改密码
    :param: old_password: 旧密码
    :param: password: 密码
    :param: check_pwd: 二次验证密码
    :return: {
        "data": null,
        "msg": "OK",
        "status": 200
    }
    """
    password: PasswordModel = PasswordModel.get_parameters()
    if password.password != password.check_pwd:
        raise HttpError(400, '两次填写的密码不一致')
    database.update_user_password(uuid=session.get('uuid'), password=password.password, old_pwd=password.old_pwd)
    return Result.OK().build()


@user_bp.route('/info', methods=['PUT'])
def update_user_info():
    # if session.get('user_id') != 1 and session.get('user_id') != user_id:
    #     raise HttpError(403, '没有权限修改此用户信息')
    pass


@user_bp.route('', methods=['GET'])
def get_user_info():
    """
    获取用户信息
    :return: {
        "data": {
            "username": "用户名",
            "uuid": "uuid"
        },
        "msg": "OK",
        "status": 200
    }
    """
    return Result.OK().data(database.get_user_info(session.get('uuid'))).build()
