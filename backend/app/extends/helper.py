import typing


def check_username(username: str) -> typing.Union[bool, str]:
    username_len = len(username)
    if username_len < 6 or username_len > 12:
        return '用户名必须是6到12个字符'
    return True


def check_password(password: str) -> typing.Union[bool, str]:
    if len(password) < 6:
        return '密码必须大于6位'
    return True


def check_post_or_comment_content(content: str) -> typing.Union[bool, str]:
    content_len = len(content)
    if content is None or content_len == 0:
        return '请输入帖子或评论内容'
    elif content_len > 120:
        return '帖子或评论长度不能超过120字'
    return True
