from flask import Blueprint, request, session
from werkzeug.datastructures import FileStorage
import uuid

from app.models.controller import *
from app.services import database
from app.extends.result import Result
from app.extends.error import HttpError
from app.config import BaseConfig

users_bp = Blueprint('users', __name__, url_prefix='/users')


# 注册
@users_bp.route('', methods=['POST'])
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
@users_bp.route('/me/password', methods=['PUT'])
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


@users_bp.route('/me/info', methods=['PUT'])
def update_user_info():
    """
    修改用户信息
    :return: {
        "data": null,
        "msg": "OK",
        "status": 200
    }
    """
    user_detail: UserDetailModel = UserDetailModel.get_parameters()
    database.update_user_detail(uuid=session.get('uuid'), user_detail=user_detail.to_dict())
    return Result.OK().build()


@users_bp.route('/me/avatar', methods=['PUT'])
def update_user_avatar():
    """
    上传头像
    :return: {
        "data": "头像地址",
        "msg": "OK",
        "status": 200
    }
    """
    avatar: FileStorage = request.files.get('avatar')
    print(avatar)
    if avatar is None:
        raise HttpError(400, '上传头像失败')
    extension_name = avatar.filename.split('.')[-1]
    if extension_name not in ['png', 'jpg', 'jpeg', 'gif']:
        raise HttpError(400, '目前只支持jpg, png, gif格式')

    filename = uuid.uuid4().hex + '.' + extension_name
    print(filename)

    path = BaseConfig.upload_dir + filename
    avatar.save(path)
    database.update_avatar(session.get('uuid'), filename)
    filename = 'default.jpg'
    return Result.OK().data(filename).build()


@users_bp.route('')
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
    uuid = request.args.get('uuid')
    username = request.args.get('username')

    if uuid is None and username is None:
        uuid = session.get('uuid')

    return Result.OK().data(database.get_user_info(uuid, username)).build()


@users_bp.route('/search')
def search_users():
    """
    查找用户
    :return: {
        "data": [
            {
                "username": "用户名",
                "uuid": "uuid",
                "sex": "性别 男、女、不明",
    	        "grade": "年级 数字",
    	        "major": "专业",
    	        "description": "个人介绍",
                "posts_num": "帖子数量",
                "avatar": "头像地址"
            },
            ...
        ],
        "msg": "OK",
        "status": 200
    }
    """
    return Result.OK().data(
        database.search_users(keyword=request.args.get('keyword'), last_user_uuid=request.args.get('last_user_uuid'),
                              limit=request.args.get('limit', default=10))
    ).build()
