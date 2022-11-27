from sqlalchemy import text, engine

from app import db
from models import AppModel


class SavePost(db.Model, AppModel):
    __tablename__ = 'save_post'
    post_save_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
