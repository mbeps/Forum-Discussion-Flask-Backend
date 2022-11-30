from sqlalchemy import text, engine

from app import db
from models import AppModel


class SavePost(db.Model, AppModel):
    """SavePost's model/table relation.
    Saves a post for a user.
    
    Fields:
        `save_post_id` (int): primary key
        `post_id` (int): foreign key to `Post`'s table
        `user_id` (int): foreign key to `User`'s table
    """
    __tablename__: str = 'save_post'
    post_save_id: int = db.Column(db.Integer, primary_key=True)
    post_id: int = db.Column(db.Integer)
    user_id: int = db.Column(db.Integer)
