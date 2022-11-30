from sqlalchemy import text, engine

from app import db
from models import AppModel


class LikePost(db.Model, AppModel):
    """`LikePost`'s model/table relation.
    Captures the relationship between a `User` and a `Post`.
    
    Fields:
        `like_post_id` (int): primary key
        `post_id` (int): foreign key to `Post`'s table
        `user_id` (int): foreign key to `User`'s table
    """
    __tablename__ = 'like_post'
    post_like_id: int = db.Column(db.Integer, primary_key=True)
    post_id: int = db.Column(db.Integer)
    user_id: int = db.Column(db.Integer)
