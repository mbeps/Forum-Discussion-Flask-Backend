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

