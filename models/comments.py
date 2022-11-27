
from app import db
from models import AppModel
import datetime
from models.community import Community


class Comment(db.Model, AppModel):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    comment = db.Column(db.String(255))
    create_dttm = db.Column(db.Date, default=datetime.date.today())

    @staticmethod
    def get_comments_by_post_id(post_id):
        return Comment.query.filter_by(post_id=post_id).all()

    @staticmethod
    def get_comments_by_id(comment_id):
        return Comment.query.filter_by(comment_id=comment_id).first()
