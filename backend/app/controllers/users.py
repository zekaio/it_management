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
    session['username'] = user_detail.username
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
    if avatar is None:
        raise HttpError(400, '上传头像失败')
    extension_name = avatar.filename.split('.')[-1]
    if extension_name not in ['png', 'jpg', 'jpeg', 'gif']:
        raise HttpError(400, '目前只支持jpg, png, gif格式')

    filename = uuid.uuid4().hex + '.' + extension_name

    path = BaseConfig.avatar_dir + filename
    avatar.save(path)
    database.update_avatar(session.get('uuid'), filename)
    return Result.OK().data(filename).build()


@users_bp.route('/me/bg', methods=['PUT'])
def update_user_background_image():
    """
    上传背景
    :return: {
        "data": "背景地址",
        "msg": "OK",
        "status": 200
    }
    """
    img: FileStorage = request.files.get('bg')
    if img is None:
        raise HttpError(400, '上传头像失败')
    extension_name = img.filename.split('.')[-1]
    if extension_name not in ['png', 'jpg', 'jpeg', 'gif']:
        raise HttpError(400, '目前只支持jpg, png, gif格式')

    filename = uuid.uuid4().hex + '.' + extension_name

    path = BaseConfig.bg_dir + filename
    img.save(path)
    database.update_bg(session.get('uuid'), filename)
    return Result.OK().data(filename).build()


@users_bp.route('')
def get_user_info():
    """
    获取用户信息
    :return: {
        "data": {
            "username": "用户名",
            "uuid": "uuid",
            "sex": "性别 男、女、不明",
    	    "grade": "年级 数字",
    	    "major": "专业",
    	    "description": "个人介绍",
            "posts_num": "帖子数量",
            "avatar": "头像文件名",
            "follow_status": "boolean 是否关注",
            "fans_num": "粉丝数量",
            "follow_num": "关注的人的数量"
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


@users_bp.route('/me/follow', methods=['PUT'])
def follow_user():
    """
    关注或取关用户
    """
    data: dict = request.get_json(force=True)

    username: str = data.get('username')
    if username is None:
        raise HttpError(400, '用户名错误')
    if username == session.get('username'):
        raise HttpError(400, '无法关注自己')

    status: bool = data.get('status')
    if status is None:
        raise HttpError(400, '请选择要进行的操作')

    database.follow_user(session.get('uuid'), username, status)
    return Result.OK().build()


@users_bp.route('/follow')
def get_follow_list():
    """
    获取关注的人的列表
    :return: {
        "data": [
            {
            "follow_id": "follow_id",
            "user_id": "用户id",
            "user_username": "用户名",
            "user_avatar": "头像地址",
            "user_description": "个人简介",
            "followed_user_id": "被关注用户id",
            "followed_user_username": "被关注用户用户名",
            "followed_user_avatar": "被关注用户头像",
            "followed_user_description": "被关注用户个人简介",
            "status": "true为已关注，false为未关注"
            },
            ...
        ],
        "msg": "OK",
        "status": 200
    }
    """
    uuid = request.args.get('uuid')
    username = request.args.get('username')
    last_follow_id = request.args.get('last_follow_id', default=0)
    limit = request.args.get('limit', default=20)

    if uuid is None and username is None:
        uuid = session.get('uuid')

    return Result.OK().data(database.get_follow_list(uuid, username, last_follow_id, limit)).build()


@users_bp.route('/fans')
def get_fans_list():
    """
    获取粉丝列表
    :return: {
        "data": [
            {
            "follow_id": "follow_id",
            "user_id": "用户id",
            "user_username": "用户名",
            "user_avatar": "头像地址",
            "user_description": "个人简介",
            "followed_user_id": "被关注用户id",
            "followed_user_username": "被关注用户用户名",
            "followed_user_avatar": "被关注用户头像",
            "followed_user_description": "被关注用户个人简介",
            "status": "true为已关注，false为未关注"
            },
            ...
        ],
        "msg": "OK",
        "status": 200
    }
    """
    uuid = request.args.get('uuid')
    username = request.args.get('username')
    last_follow_id = request.args.get('last_follow_id', default=0)
    limit = request.args.get('limit', default=20)

    if uuid is None and username is None:
        uuid = session.get('uuid')

    return Result.OK().data(database.get_fans_list(uuid, username, last_follow_id, limit)).build()
