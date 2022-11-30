from sqlalchemy import text, engine

from app import db
from models import AppModel
from models.community import Community


class CommunitySubscribe(db.Model, AppModel):
    """`CommunitySubscribe`'s model/table.
    Captures the relationship between a `User` and a `Community`.

    Fields:
        `community_subscribe_id` (int): primary key
        `community_id` (int): foreign key to `Community`'s table
        `user_id` (int): foreign key to `User`'s table
    """    
    __tablename__: str = 'community_subscribe'
    community_subscribe_id: int = db.Column(db.Integer, primary_key=True)
    community_id: int = db.Column(db.Integer)
    user_id: int = db.Column(db.Integer)

    @staticmethod
    def get_all_subscribed_communities(user_id: int):
        """Gets all communities a user is subscribed to.

        Args:
            user_id (int): user ID for which to get communities from

        Returns:
            list[Community]: list of communities to be returned
        """        
        return Community.query.join(
            CommunitySubscribe,
            CommunitySubscribe.community_id == Community.community_id
        ).filter(
            CommunitySubscribe.user_id == user_id
        ).all() # returns a list of Community objects

    @staticmethod
    def get_community_by_user_id(user_id: int):
        """Gets a community related to a user.

        Args:
            user_id (int): user from which to get community from

        Returns:
            list[Community]: communities related to user to be returned
        """        
        return Community.query.filter_by(user_id=user_id).all()

    @staticmethod
    def unsubscribe_from_community(community_id: int, user_id: int):
        """Unsubscribes a user from a community.

        Args:
            community_id (int): community from which to unsubscribe from
            user_id (int): user to unsubscribe from community
        """        
        community_subscribe: CommunitySubscribe = CommunitySubscribe.query.filter_by(
            community_id=community_id, 
            user_id=user_id).first()
        db.session.delete(community_subscribe)
        db.session.commit()