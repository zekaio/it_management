from app.extensions import db, Model


class Follow(Model):
    __tablename__ = 'follow'

    follow_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, index=True, comment='用户id')
    user_username = db.Column(db.String(255), nullable=False, comment='用户名')
    user_avatar = db.Column(db.String(255), nullable=False, comment='头像')
    user_description = db.Column(db.String(255), nullable=False, comment='个人介绍')

    followed_user_id = db.Column(db.Integer, index=True, comment='被关注的人的id')
    followed_user_username = db.Column(db.String(255), nullable=False, comment='被关注的人的用户名')
    followed_user_avatar = db.Column(db.String(255), nullable=False, comment='被关注的人的头像')
    followed_user_description = db.Column(db.String(255), nullable=False, comment='被关注的人的个人介绍')
    status = db.Column(db.Boolean, index=True, default=True, comment='1：正在关注，0：取消关注')

    def to_dict(self):
        return dict(
            follow_id=self.follow_id,
            user_id=self.user_id,
            user_username=self.user_username,
            user_avatar=self.user_avatar,
            user_description=self.user_description,
            followed_user_id=self.followed_user_id,
            followed_user_avatar=self.followed_user_avatar,
            followed_user_username=self.followed_user_username,
            followed_user_description=self.followed_user_description,
            status=self.status
        )
