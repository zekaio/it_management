class HttpError(Exception):
    def __init__(self, status_code, message, data=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.data = data

    def to_dict(self):
        return {
            'status': self.status_code,
            'message': self.message,
            'data': self.data
        }
