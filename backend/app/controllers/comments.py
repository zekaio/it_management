from flask import Blueprint, request, session
from werkzeug.datastructures import FileStorage

from app.extends.result import Result
from app.services import database
from app.extends.helper import check_post_or_comment_content, save_image
from app.extends.error import HttpError
from app.config import BaseConfig

comments_bp = Blueprint('comments', __name__, url_prefix='/comments')


@comments_bp.route('', methods=['GET'])
def get_comments():
    """
    通过id获取某个帖子或评论的多条评论
    :param: parent_id: 被评论的帖子或评论的id
    :param: type: 是什么的评论，0是帖子，1是评论
    :param: last_id: 已获取评论中最后一个评论的id，默认为0
    :param: limit: 要获取的数目， 默认为5
    :return: {
        "data": {
            "comments": [
                {
                    "comment_id": "评论id",
                    "parent_id": "被评论的帖子或评论的id",
                    "type": "是什么的评论，0是帖子，1是评论",
                    "content": "评论内容",
                    "comments_num": "评论数目",
                    "username": "发帖人用户名",
                    "uuid": "发帖人uuid",
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
    ret = database.get_comments(
        parent_id=request.args.get('parent_id'),
        _type=request.args.get('type'),
        last_comment_id=request.args.get('last_id', default=0),
        limit=request.args.get('limit', default=5))
    return Result.OK().data({
        'comments': ret[0], 'comments_num': ret[1]
    }).build()


@comments_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id: int):
    """
    通过id获取一条评论的详细信息和它的评论
    :param comment_id: 评论id
    :param: last_comment_id: 最后一个评论的id，默认为0
    :param: limit: 要获取的评论数目， 默认为5
    :return: {
            "data": {
            "comment_id": "评论id",
            "parent_id": "被评论的帖子或评论的id",
            "type": "是什么的评论，0是帖子，1是评论",
            "content": "评论内容",
            "comments_num": "评论数目",
            "username": "发帖人用户名",
            "uuid": "发帖人uuid",
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
        database.get_comment(
            comment_id=comment_id,
            last_comment_id=request.args.get('last_comment_id', default=0),
            limit=request.args.get('limit', default=5)
        )
    ).build()


@comments_bp.route('', methods=['POST'])
def save_comment():
    """
    发表评论
    :param: parent_id: 被评论的帖子或评论的id
    :param: type: 是什么的评论，0是帖子，1是评论
    :param: content: 内容
    :return: {
        "data": {
            "comment_id": "评论id"
        },
        "msg": "OK",
        "status": 200
    }
    """
    content: str = request.form.get('content')
    ret = check_post_or_comment_content(content)
    if ret is not True:
        raise HttpError(400, ret)

    parent_id: int = request.form.get('parent_id')
    _type: int = request.form.get('type')

    img: FileStorage = request.files.get('img')
    img_name = None if img is None else save_image(BaseConfig.comment_image_dir, img)

    database.save_comment(content=content, parent_id=parent_id, _type=_type, img_name=img_name,
                          uuid=session.get('uuid'))

    return Result.OK().build()


@comments_bp.route('/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id: int):
    """
    修改评论
    :param comment_id: 评论id
    :param: content: 新内容
    :return: {
        "data": {
            "comment_id": "评论id"
        },
        "msg": "OK",
        "status": 200
    }
    """
    content: str = request.form.get('content')
    ret = check_post_or_comment_content(content)
    if ret is not True:
        raise HttpError(400, ret)

    img: FileStorage = request.files.get('img')
    img_name = None if img is None else save_image(BaseConfig.comment_image_dir, img)

    database.update_comment(content=content, img_name=img_name, comment_id=comment_id, uuid=session.get('uuid'))

    return Result.OK().build()


@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id: int):
    """
    删除评论
    :param comment_id: 评论id
    :return: {
        "data": null,
        "msg": "OK",
        "status": 200
    }
    """
    database.delete_comment(comment_id, session.get('uuid'))

    return Result.OK().build()
