from sqlalchemy import func

from app.extensions import db, Model


class Comment(Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, index=True, comment='评论用户id')
    parent_id = db.Column(db.Integer, default=None, comment='被评论的帖子或评论的id')
    root_id = db.Column(db.Integer, default=None, comment='对帖子的评论是帖子id，否则是根评论id')
    post_id = db.Column(db.Integer, default=None, comment='帖子的id')
    type = db.Column(db.Integer, default=0, comment='是什么的评论，0是帖子，1是评论')
    content = db.Column(db.String(120), nullable=False, comment='内容')
    comments_num = db.Column(db.Integer, default=0, comment='评论数量')
    img_name = db.Column(db.String(255), nullable=True, default=None, comment='评论图片')

    updated_at = db.Column(db.DateTime, server_default=func.now(), comment='修改时间')
    deleted_at = db.Column(db.DateTime, nullable=True, default=None, comment='删除时间')

    __table_args__ = (
        db.Index('ix_parent_id_type', 'parent_id', 'type'),
    )

    def to_dict(self):
        return {
            'comment_id': self.comment_id,
            'parent_id': self.parent_id,
            'root_id': self.root_id,
            'post_id': self.post_id,
            'type': self.type,
            'content': self.content,
            'comments_num': self.comments_num,
            'img_name': self.img_name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def update_time(self):
        self.updated_at = func.now()
