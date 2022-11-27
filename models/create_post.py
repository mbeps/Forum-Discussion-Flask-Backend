from app import db
from models import AppModel, User, CommunitySubscribe
from sqlalchemy.orm import relationship
import datetime


class Post(db.Model, AppModel):
    __tablename__ = 'create_post'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    community_id = db.Column(db.Integer)
    post_name = db.Column(db.String(20))
    description = db.Column(db.String(256))
    create_dttm = db.Column(db.DateTime, default=datetime.datetime.now())

    @staticmethod
    def get_posts_by_user_id(user_id):
        return Post.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_posts_by_community_id(community_id):
        return Post.query.filter_by(community_id=community_id).all()