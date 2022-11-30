from app import db
from models import AppModel, User, CommunitySubscribe
from sqlalchemy.orm import relationship
import datetime


class Post(db.Model, AppModel):
    """`Post`'s model/table.

    Fields:
        `post_id` (int): primary key
        `user_id` (int): foreign key to `User`'s table
        `community_id` (int): foreign key to `Community`'s table
        `post_name`` (str): name of the post
        `description` (str): description of the post
        `create_dttm` (datetime): date and time of creation    
    """
    __tablename__: str = 'posts'
    post_id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer)
    community_id: int = db.Column(db.Integer)
    post_name: str = db.Column(db.String(20))
    description: str = db.Column(db.String(256))
    create_dttm: datetime.datetime = db.Column(db.DateTime, default=datetime.datetime.now())

    @staticmethod
    def get_posts_by_user_id(user_id: int):
        """Gets all posts created by a user.

        Args:
            user_id (int): user for which to get posts from

        Returns:
            list[Post]: posts created by user
        """        
        return Post.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_posts_by_community_id(community_id: int):
        """Gets all posts related to a community.

        Args:
            community_id (int): community for which to get posts from        
        """
        return Post.query.filter_by(community_id=community_id).all()

    @staticmethod
    def delete_post(post_id: int):
        """Deletes a post.

        Args:
            post_id (int): post to be deleted
        """        
        post: Post = Post.query.filter_by(post_id=post_id).first()
        db.session.delete(post)
        db.session.commit()