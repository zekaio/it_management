import typing


class Result:
    status = None
    msg = None
    _data = None

    @classmethod
    def data(cls, _data: typing.Union[dict, str]):
        cls._data = _data
        return cls

    @classmethod
    def build(cls):
        return {
            'status': cls.status,
            'msg': cls.msg,
            'data': cls._data
        }

    @classmethod
    def OK(cls):
        cls.status = 200
        cls.msg = 'OK'
        return cls

    # def BAD(cls):
    #     cls.status = 400
    #     cls.msg = 'Bad Request'
    #     return cls
