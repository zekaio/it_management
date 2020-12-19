from app.extends.helper import check_username, check_password, check_sex, check_description
from app.extends.check import BaseModel, Parameter


class PasswordModel(BaseModel):
    password = Parameter(str, check_func=check_password)
    old_pwd = Parameter(str, check_func=check_password, required=False)
    check_pwd = Parameter(str, check_func=check_password, required=False)


class UserModel(PasswordModel):
    username = Parameter(str, check_func=check_username)


class UserDetailModel(BaseModel):
    username = Parameter(str, check_func=check_username)
    sex = Parameter(str, check_func=check_sex)
    grade = Parameter(int)
    major = Parameter(str)
    description = Parameter(str, check_func=check_description)
