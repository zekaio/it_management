import uuid
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, Model


class User(Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, comment='uuid')
    username = db.Column(db.String(255), unique=True, nullable=False, comment='用户名')
    password = db.Column(db.String(255), nullable=False, comment='密码')

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
            'uuid': self.uuid
        }
