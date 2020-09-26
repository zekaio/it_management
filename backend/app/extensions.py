"""
扩展
"""
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import Query, Session

cors = CORS(supports_credentials=True)
migrate = Migrate()


class _SQLAlchemy(SQLAlchemy):
    session: Session


db = _SQLAlchemy()


class Model(db.Model):
    __abstract__ = True

    # __table_args__ = {
    #     'mysql_collate': 'utf8mb4_general_ci'
    # }

    query: Query

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='修改时间')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
