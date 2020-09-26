from .check_login import check_login


def before_request():
    check_login()
