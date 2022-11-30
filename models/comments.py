
from app import db
from models import AppModel
import datetime
from models.community import Community


class Comment(db.Model, AppModel):
    """`Comment`'s model/table. 
    
    Fields:
        `comment_id` (int): primary key
        `post_id` (int): foreign key to `Post`'s table
        `user_id` (int): foreign key to `User`'s table
        `comment` (str): comment
        `created_at` (datetime): date and time of creation
    """    
    __tablename__: str = 'comments'
    comment_id: int = db.Column(db.Integer, primary_key=True)
    post_id: int = db.Column(db.Integer)
    user_id: int = db.Column(db.Integer)
    comment: str = db.Column(db.String(255))
    create_dttm: datetime.date = db.Column(db.Date, default=datetime.date.today())

    @staticmethod
    def get_comments_by_post_id(post_id: int):
        """Gets a comment related to a post.

        Args:
            post_id (int): post from which to get comment from

        Returns:
            list[Comment]: comment to be returned
        """        
        return Comment.query.filter_by(post_id=post_id).all()

    @staticmethod
    def get_comments_by_id(comment_id: int):
        """Gets a comment by its ID.

        Args:
            comment_id (int): comment ID for which to get comment from

        Returns:
            Comment: comment to be returned
        """        
        return Comment.query.filter_by(comment_id=comment_id).first() 

    @staticmethod
    def get_comments_by_user_id(user_id: int):
        """Gets a comment related to a user.

        Args:
            user_id (int): user from which to get comment from

        Returns:
            Comment: comment to be returned
        """        
        return Comment.query.filter_by(user_id=user_id).all()

    @staticmethod
    def delete_comment_by_id(comment_id: int):
        """Deletes a comment by its ID.

        Args:
            comment_id (int): comment ID for which to delete comment from

        Returns:
            Comment: comment to be deleted
        """        
        comment = Comment.query.filter_by(comment_id=comment_id).first()
        db.session.delete(comment)
        db.session.commit()
