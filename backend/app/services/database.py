import typing

from app.extends.error import HttpError
from app.extensions import db
from app.models.database import *


def _get_user(**kwargs) -> User:
    """
    查找用户
    :param kwargs: 键值对形式，查找条件
    :return: User
    """
    return (
        User
            .query
            .filter_by(**kwargs)
            .first()
    )


def _get_post(**kwargs) -> Post:
    """
    查找帖子
    :param kwargs: 键值对形式，查找条件
    :return: Post
    """
    return (
        Post
            .query
            .filter_by(**kwargs)
            .first()
    )


def _get_comment(**kwargs) -> Comment:
    """
    查找评论
    :param kwargs: 键值对形式，查找条件
    :return: Comment
    """
    return (
        Comment
            .query
            .filter_by(**kwargs)
            .first()
    )


def _get_comments(last_comment_id: int = 0, limit: int = 5, **kwargs) -> typing.List[dict]:
    """
    获取评论
    :param last_comment_id: 最后一条评论的id
    :param limit: 要获取的数目
    :param kwargs: 键值对形式，查找条件
    :return: [
        {
            "comment_id": "评论id",
            "parent_id": "被评论的帖子或评论的id",
            "type": "是什么的评论，0是帖子，1是评论",
            "content": "评论内容",
            "comments_num": "评论数量",
            "username": "发帖人用户名",
            "uuid"': "发帖人uuid"
        }
        ...
    ]
    """
    if int(last_comment_id):
        query = Comment.query.filter(Comment.comment_id < last_comment_id)
    else:
        query = Comment.query
    comments: typing.List[Comment] = (
        query
            .filter_by(**kwargs)
            .order_by(Comment.comment_id.desc())
            .limit(limit)
            .all()
    )

    ret = []

    for comment in comments:
        ret.append(_get_post_or_comment_info(comment))

    return ret


def _get_post_or_comment_info(obj: typing.Union[Post, Comment]) -> dict:
    """
    获取完整的帖子或评论信息
    :param obj: Post or Comment object
    :return: {
        "username": "发帖人用户名",
        "uuid"': "发帖人uuid",
        **Post.to_dict() or **Comment.to_dict()
    }
    """
    info: dict = obj.to_dict()
    user: User = _get_user(user_id=obj.user_id)
    if user is None:
        user_info = {}
    else:
        user_info: dict = user.to_dict()

    return {
        **info,
        **user_info
    }


def create_user(username: str, password: str) -> tuple:
    """
    创建用户
    :param username: 用户名
    :param password: 密码
    :return: (uuid, username)
    """
    user: User = _get_user(username=username)
    if user:
        raise HttpError(409, '用户已存在')
    user: User = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user.uuid, user.username


def update_user_password(uuid: str, password: str, old_pwd: str):
    """
    修改密码
    :param uuid: uuid
    :param old_pwd: 旧密码
    :param password: 新密码

    """
    user: User = _get_user(uuid=uuid)
    if user is None:
        raise HttpError(404, '用户不存在')
    if not user.check_password(old_pwd):
        raise HttpError(400, '旧密码错误')
    user.update_password(password)
    db.session.commit()


def user_login(username: str, password: str) -> tuple:
    """
    用户登录
    :param username: 用户名
    :param password: 密码
    :return: (uuid, username)
    """
    user: User = _get_user(username=username)
    if user is None or not user.check_password(password):
        raise HttpError(400, '用户名或密码错误')

    return user.uuid, user.username


def get_user_info(uuid: str) -> dict:
    """
    获取用户信息
    :param uuid: uuid
    :return: {
        "username": "用户名",
        "uuid": "uuid"
    }
    """
    user: User = _get_user(uuid=uuid)
    if user is None:
        raise HttpError(404, '用户不存在')

    return user.to_dict()


def get_posts(uuid: str, keyword: str, last_id: int, limit: int) -> typing.List[dict]:
    """
    获取多个帖子
    :param uuid: uuid
    :param keyword: 搜索关键词
    :param last_id: 已获取帖子中最后一个帖子的id
    :param limit: 要获取的数目
    :return: [
        {
            "post_id": "帖子id",
            "username": "发帖人用户名",
            "uuid"': "发帖人uuid",
            "content"': "内容",
            "comments_num": "评论数目",
            "comments": [
                {
                    "comment_id": "评论id",
                    "parent_id": "被评论的帖子或评论的id",
                    "type": "是什么的评论，0是帖子，1是评论",
                    "content": "评论内容",
                    "comments_num": "评论数目",
                    "username": "发帖人用户名",
                    "uuid"': "发帖人uuid"
                }
                ...
            ]
        },
        ...
    ]
    """
    query = (
        Post
            .query
            .order_by(Post.post_id.desc())
    )

    if uuid:
        user: User = _get_user(uuid=uuid)
        if not user:
            raise HttpError(404, '用户不存在')
        query = query.filter_by(user_id=user.user_id)

    if keyword:
        query = query.filter(Post.content.like(f'%{keyword}%'))

    if int(last_id):
        query = query.filter(Post.post_id < last_id)

    posts: typing.List[Post] = (
        query
            .limit(limit)
            .all()
    )
    ret = []
    for post in posts:
        post_info: dict = _get_post_or_comment_info(post)
        post_info['comments'] = _get_comments()
        ret.append(post_info)

    return ret


def get_post(post_id: int, last_comment_id: int = 0, limit: int = 5):
    """
    通过id获取帖子信息和评论
    :param post_id: 帖子id
    :param last_comment_id: 最后一个评论的id
    :param limit: 要获取的数量
    :return: {
        "post_id": "帖子id",
        "username": "发帖人用户名",
        "uuid"': "发帖人uuid",
        "content"': "内容",
        "comments_num": "评论数目",
        "comments": [
            {
                "id": "评论id",
                "parent_id": "被评论的帖子或评论的id",
                "type": "是什么的评论，0是帖子，1是评论",
                "content": "评论内容",
                "comments_num": "评论数目",
                "username": "发帖人用户名",
                "uuid"': "发帖人uuid"
            }
            ...
        ]
    }

    """
    post: Post = _get_post(post_id=post_id)

    if post is None:
        raise HttpError(404, '帖子不存在')

    post_info: dict = _get_post_or_comment_info(post)

    comments: typing.List[dict] = _get_comments(last_comment_id, limit, type=0, parent_id=post_id)

    return {
        **post_info,
        'comments': comments
    }


def save_post(content: str, uuid: str) -> int:
    """
    保存帖子
    :param content: 帖子内容
    :param uuid: 发帖人uuid
    :return: post_id
    """
    user: User = _get_user(uuid=uuid)
    if not User:
        raise HttpError(404, '用户不存在')

    post = Post(content=content, user_id=user.user_id)
    db.session.add(post)
    db.session.commit()

    return post.post_id


def update_post(content: str, uuid: str, post_id: int) -> int:
    """
    修改帖子
    :param content: 新内容
    :param uuid: 发贴人uuid
    :param post_id: 帖子id
    :return: post_id
    """
    post: Post = _get_post(post_id=post_id)
    if not post:
        raise HttpError(404, '帖子不存在')

    post_info: dict = _get_post_or_comment_info(post)
    if not uuid == post_info.get('uuid'):
        raise HttpError(403, '没有权限修改该帖子')

    post.content = content
    db.session.commit()

    return post.post_id


def delete_post(post_id: int, uuid: str):
    """
    删除帖子
    :param post_id: 帖子id
    :param uuid: 发帖人uuid
    """
    post: Post = _get_post(post_id=post_id)
    if not post:
        raise HttpError(404, '帖子不存在')

    post_info = _get_post_or_comment_info(post)
    if not uuid == post_info.get('uuid'):
        raise HttpError(403, '没有权限删除该帖子')

    db.session.delete(post)
    db.session.commit()


def get_comments(parent_id: int, _type: int, limit: int = 5, last_comment_id: int = 0) -> (typing.List[dict], int):
    """
    通过id获取某个帖子或评论的多条评论
    :param: parent_id: 被评论的帖子或评论的id
    :param: _type: 是什么的评论，0是帖子，1是评论
    :param: last_id: 已获取评论中最后一个评论的id，默认为0
    :param: limit: 要获取的数目， 默认为5
    :return: [
        {
            "comment_id": "评论id",
            "parent_id": "被评论的帖子或评论的id",
            "type": "是什么的评论，0是帖子，1是评论",
            "content": "评论内容",
            "comments_num": "评论数目",
            "username": "发帖人用户名",
            "uuid": "发帖人uuid"
        }
        ...
    ]
    """
    if int(_type):
        obj: Comment = (
            Comment.query.get(parent_id)
        )
    else:
        obj: Post = (
            Post.query.get(parent_id)
        )
    return _get_comments(last_comment_id, limit, parent_id=parent_id, type=_type), obj.comments_num


def get_comment(comment_id, last_comment_id: int = 0, limit: int = 5):
    """
    通过id获取一条评论的详细信息和它的评论
    :param comment_id: 评论id
    :param last_comment_id: 最后一个评论的id
    :param limit: 要获取的数量
    :return: {
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
                "uuid"': "发帖人uuid"
            }
            ...
        ]
    }
    """
    comment: Comment = _get_comment(comment_id=comment_id)

    if comment is None:
        raise HttpError(404, '评论不存在')

    comment_info: dict = _get_post_or_comment_info(comment)

    comments: typing.List[dict] = _get_comments(last_comment_id, limit, type=1, parent_id=comment_id)

    return {
        **comment_info,
        'comments': comments
    }


def save_comment(content: str, parent_id: int, _type: int, uuid: str) -> (int, str, str):
    """
    发表评论
    :param content: 评论内容
    :param parent_id: 被评论的帖子或评论的id
    :param _type: 是什么的评论，0是帖子，1是评论
    :param uuid: 发表评论的用户的uuid
    :return: comment_id
    """
    user: User = _get_user(uuid=uuid)
    if not User:
        raise HttpError(404, '用户不存在')
    if int(_type):
        comment: Comment = _get_comment(comment_id=parent_id)
        if not comment:
            raise HttpError(404, '评论不存在')
        comment.comments_num = comment.comments_num + 1
    else:
        post: Post = _get_post(post_id=parent_id)
        if not post:
            raise HttpError(404, '帖子不存在')
        post.comments_num = post.comments_num + 1

    comment = Comment(user_id=user.user_id, parent_id=parent_id, type=_type, content=content)
    db.session.add(comment)
    db.session.commit()

    return comment.comment_id, user.username, user.uuid, comment.created_at


def update_comment(comment_id: int, content: str, uuid: str) -> int:
    """
    更新评论
    :param comment_id: 评论id
    :param content: 新内容
    :param uuid: uuid
    :return: comment_id
    """
    comment: Comment = _get_comment(comment_id=comment_id)
    if not comment:
        raise HttpError(404, '评论不存在')

    comment_info: dict = _get_post_or_comment_info(comment)
    if not uuid == comment_info.get('uuid'):
        raise HttpError(403, '没有权限修改该评论')

    comment.content = content
    db.session.commit()

    return comment.comment_id


def delete_comment(comment_id: int, uuid: str):
    """
    删除评论
    :param comment_id: 评论id
    :param uuid: uuid
    """
    comment: Comment = _get_comment(comment_id=comment_id)
    if not comment:
        raise HttpError(404, '评论不存在')

    comment_info: dict = _get_post_or_comment_info(comment)
    if not uuid == comment_info.get('uuid'):
        raise HttpError(403, '没有权限删除该评论')

    if int(comment.type):
        parent_comment: Comment = _get_comment(comment_id=comment.parent_id)
        parent_comment.comments_num = parent_comment.comments_num - 1
    else:
        parent_post: Post = _get_post(post_id=comment.parent_id)
        parent_post.comments_num = parent_post.comments_num - 1

    db.session.delete(comment)
    db.session.commit()
