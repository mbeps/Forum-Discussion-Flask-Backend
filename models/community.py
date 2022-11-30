from app import db
from models import AppModel


class Community(db.Model, AppModel):
    """`Community`'s model/table.
    
    Fields:
        `community_id` (int): primary key
        `user_id` (int): foreign key to `User`'s table
        `community_name` (str): community name
        `community_description` (str): community description
    """
    __tablename__: str = 'communities'
    community_id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer)
    community_name: str = db.Column(db.String(20))
    description: str = db.Column(db.String(256))

    @staticmethod
    def get_all_communities():
        """Gets all communities in the database.

        Returns:
            list[Community]: list of communities to be returned
        """
        return Community.query.filter()

    @staticmethod
    def get_community_by_user_id(user_id: int):
        """Gets all communities related to a user.
        Args:
            user_id (int): user from which to get communities from
        Returns:
            Community: communities related to user to be returned
        """
        return Community.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_community_by_community_id(community_id: int):
        """Gets a community by its ID.

        Args:
            community_id (int): community to get

        Returns:
            Community: community to be returned
        """        
        return Community.query.filter_by(community_id=community_id).first()

    @staticmethod
    def delete_community(community_id: int):
        """Deletes a community.

        Args:
            community_id (int): community to delete
        """        
        community: Community = Community.get_community_by_community_id(community_id) # get community by community_id
        db.session.delete(community) # delete community from database
        db.session.commit() # commit changes to database