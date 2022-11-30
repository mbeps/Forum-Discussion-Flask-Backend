from app import db
from models import AppModel


class User(db.Model, AppModel):
    """`User`'s model/table relation.

    Fields:
        `user_id` (int): primary key
        `username` (str): username
        `password` (str): password
        `email` (str): email
        `is_authenticated` (bool): is authenticated
        `code` (str): code    
    """
    __tablename__: str = 'user'
    user_id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(20))
    email: str = db.Column(db.String(256))
    password: str = db.Column(db.String(255))
    is_authenticated: bool = db.Column(db.Boolean, default=False)
    code: int = db.Column(db.String(20))
