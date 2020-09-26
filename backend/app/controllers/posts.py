from flask import Blueprint, request, session

from app.services import database
from app.extends.result import Result
from app.extends.error import HttpError
from app.extends.helper import check_post_or_comment_content

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')


@posts_bp.route('', methods=['GET'])
def get_posts():
    """
    获取多个帖子
    :param: uuid: uuid
    :param: last_id: 已获取帖子中最后一个帖子的id，默认为0
    :param: limit: 要获取的数目， 默认为5
    :return: {
        "data": {
            "posts": [
                {
                    "post_id": "帖子id",
                    "username": "发帖人用户名",
                    "uuid": "发帖人uuid",
                    "content": "内容",
                    "comments_num": "评论数目",
                    "created_at": "创建时间",
                    "updated_at": "修改时间"
                    "comments": [
                        {
                            "comment_id": "评论id",
                            "parent_id": "被评论的帖子或评论的id",
                            "type": "是什么的评论，0是帖子，1是评论",
                            "content": "评论内容",
                            "comments_num": "评论数目",
                            "username": "发帖人用户名",
                            "uuid"': "发帖人uuid",
                            "created_at": "创建时间",
                            "updated_at": "修改时间"
                        }
                        ...
                    ]
                },
                ...
            ]
        }
        "msg": "OK",
        "status": 200
    }
    """
    return Result.OK().data(
        database.get_posts(
            uuid=request.args.get('uuid',default=None),
            last_id=request.args.get('last_id', default=0),
            limit=request.args.get('limit', default=5))
    ).build()


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id: int):
    """
    通过id获取帖子
    :param post_id: 帖子id
    :param: last_comment_id: 最后一个评论的id，默认为0
    :param: limit: 要获取的评论数目， 默认为5
    :return: {
        "data": {
            "post_id": "帖子id",
            "username": "发帖人用户名",
            "uuid": "发帖人uuid",
            "content": "内容",
            "comments_num": "评论数目",
            "created_at": "创建时间",
            "updated_at": "修改时间",
            "comments": [
                {
                    "id": "评论id",
                    "parent_id": "被评论的帖子或评论的id",
                    "type": "是什么的评论，0是帖子，1是评论",
                    "content": "评论内容",
                    "comments_num": "评论数目",
                    "username": "发帖人用户名",
                    "uuid"': "发帖人uuid",
                    "created_at": "创建时间",
                    "updated_at": "修改时间"
                }
                ...
            ]
        },
        "msg": "OK",
        "status": 200
    }
    """
    return Result.OK().data(
        database.get_post(
            post_id=post_id,
            last_comment_id=request.args.get('last_comment_id', default=0),
            limit=request.args.get('limit', default=5))
    ).build()


@posts_bp.route('', methods=['POST'])
def save_post():
    """
    发表帖子
    :param: content: 帖子内容
    :return: {
        "data": {
            "post_id": "帖子id"
        },
        "msg": "OK",
        "status": 200
    }
    """
    content: str = request.get_json(force=True).get('content')
    ret = check_post_or_comment_content(content)
    if ret is not True:
        raise HttpError(400, ret)

    post_id = database.save_post(content, session.get('uuid'))

    return Result.OK().data({
        'post_id': post_id
    }).build()


@posts_bp.route('/<int:post_id>', methods=['PUT'])
def update_post(post_id: int):
    """
    修改帖子
    :param post_id: 帖子id
    :param: content: 帖子内容
    :return: {
        "data": {
            "post_id": "帖子id"
        },
        "msg": "OK",
        "status": 200
    }
    """
    content: str = request.get_json(force=True).get('content')
    ret = check_post_or_comment_content(content)
    if ret is not True:
        raise HttpError(400, ret)

    return Result.OK().data({
        'post_id': database.update_post(
            content=content,
            uuid=session.get('uuid'),
            post_id=post_id)
    }).build()


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id: int):
    """
    删除帖子
    :param post_id: 帖子id
    :return: {
        "data": null,
        "msg": "OK",
        "status": 200
    }
    """
    database.delete_post(post_id, session.get('uuid'))

    return Result.OK().build()
