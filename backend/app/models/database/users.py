import uuid
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, Model


class User(Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, comment='uuid')
    username = db.Column(db.String(255), unique=True, nullable=False, comment='用户名')
    password = db.Column(db.String(255), nullable=False, comment='密码')
    posts_num = db.Column(db.Integer, nullable=False, default=0, comment='帖子总数')
    sex = db.Column(db.String(10), nullable=False, default='不明', comment='性别')
    grade = db.Column(db.Integer, nullable=True, default=None, comment='年级')
    major = db.Column(db.String(50), nullable=False, default='', comment='专业')
    description = db.Column(db.String(255), nullable=False, default='', comment='个人介绍')
    avatar = db.Column(db.String(255), nullable=False, default='default.jpg', comment='头像')
    bg = db.Column(db.String(255), nullable=False, default='bg.jpg', comment='背景')


    def __init__(self, username: str, password: str):
        self.username = username
        self.password = generate_password_hash(str(password))

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, str(password))

    def update_password(self, password: str):
        self.password = generate_password_hash(str(password))

    def to_dict(self) -> dict:
        return {
            'username': self.username,
            'uuid': self.uuid,
            'posts_num': self.posts_num,
            'sex': self.sex,
            'grade': self.grade,
            'major': self.major,
            'description': self.description,
            'avatar': self.avatar,
            'bg': self.bg
        }

    def update(self, **kwargs):
        self._update(_except=['user_id', 'uuid', 'password', 'posts_num'], **kwargs)
