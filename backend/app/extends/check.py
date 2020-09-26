"""
检测参数是否正确
"""
import inspect
import typing
from flask import request

from .error import HttpError


class Parameter(object):
    """
    定义参数
    """

    def __init__(self, _type: typing.Type, type_error_msg: str = None, required: bool = True,
                 check_func: typing.Callable = None, check_func_additional_params: dict = None,
                 alias: str = None
                 ):
        """
        :param _type: typing.Type 参数类型
        :param type_error_msg: str 参数类型错误时要显示的错误信息
        :param required: bool 是否必须
        :param check_func: typing.Callable 检测函数
        :param check_func_additional_params dict 检测函数中额外的参数
        :param alias str 别名
        """
        self.type = _type
        self.check_func = check_func
        self.type_error_msg = type_error_msg
        self.required = required
        self.check_func_additional_params = check_func_additional_params
        self.alias = alias
        self.value = None


class BaseModel(object):
    """
    定义参数模型

    class UserModel(BaseModel):
        username = Parameter(str)
        password = Parameter(str, check_func=check_password)
    """

    @classmethod
    def _get_attributes(cls) -> list:
        attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        return [a for a in attributes if a[0][0] != '_']

    @classmethod
    def get_parameters(cls, data: dict = None):
        """
        获取参数
        :param data: dict 和定义的参数模型对应的数据
        :return: BaseModel 返回定义的参数模型
        """

        class RetCls(cls):
            pass

        if data is None:
            data = request.get_json(force=True)

        attributes: typing.List[typing.Tuple[str, Parameter]] = cls._get_attributes()
        print(attributes)
        for key, parameter in attributes:
            # 获取参数的值
            if parameter.alias is not None:
                value = data.get(parameter.alias)
            else:
                value = data.get(key)

            # 判断参数是否有传入
            if value is None:
                if parameter.required:
                    raise HttpError(400, '缺少参数{0}'.format(key))
                else:
                    setattr(RetCls, key, value)
                    continue

            # 判断参数类型是否正确
            type_check = True
            if (value_type := type(value)) != parameter.type:
                # 如果需要的是字符串，传入的是int, float, complex，则可接受
                if parameter.type == str and not value_type in [int, float, complex]:
                    type_check = False
                # 如果需要的是int, float, complex，传入的是字符串并能转换为number，则可接受
                elif parameter.type in [int, float, complex] and value_type == str:
                    try:
                        parameter.type(value)
                    except ValueError:
                        type_check = False
            if not type_check:
                msg = parameter.type_error_msg or '应为{0}，传入了{1}'.format(parameter.type.__name__, value_type.__name__)
                raise HttpError(400, '参数“{0}”类型错误，{1}'.format(key, msg))

            # 使用检测函数判断参数是否正确
            if parameter.check_func:
                if parameter.check_func_additional_params:
                    ret = parameter.check_func(value, **parameter.check_func_additional_params)
                else:
                    ret = parameter.check_func(value)
                if ret is not True:
                    raise HttpError(400, ret)

            setattr(RetCls, key, value)

        return RetCls

    @classmethod
    def to_dict(cls) -> dict:
        attributes: typing.List[typing.Tuple[str, str]] = cls._get_attributes()
        ret = {}
        for key, value in attributes:
            if value is not None:
                ret[key] = value
        return ret
