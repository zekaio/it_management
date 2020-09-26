from sqlalchemy import func

from app.extensions import db, Model


class Post(Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, index=True, comment='发帖人id')
    content = db.Column(db.String(120), nullable=False, comment='内容')
    comments_num = db.Column(db.Integer, default=0, comment='评论数量')
    updated_at = db.Column(db.DateTime, server_default=func.now(), comment='修改时间')

    def to_dict(self):
        return {
            'post_id': self.post_id,
            'content': self.content,
            'comments_num': self.comments_num,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at' :self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def update_time(self):
        self.updated_at = func.now()
