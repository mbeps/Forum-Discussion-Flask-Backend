from sqlalchemy import text, engine

from app import db
from models import AppModel


class LikePost(db.Model, AppModel):
    __tablename__ = 'like_post'
    post_like_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
