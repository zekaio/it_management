from app.extensions import db, Model


class Follow(Model):
    __tablename__ = 'follow'

    follow_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, index=True, comment='用户id')
    followed_user_id = db.Column(db.Integer, index=True, comment='被关注的人的id')
    status = db.Column(db.Boolean, index=True, default=True, comment='1：正在关注，0：取消关注')

    def to_dict(self):
        return dict(
            follow_id=self.follow_id,
            user_id=self.user_id,
            followed_user_id=self.followed_user_id,
            status=self.status
        )
