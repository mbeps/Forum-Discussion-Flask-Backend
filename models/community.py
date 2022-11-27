from app import db
from models import AppModel


class Community(db.Model, AppModel):
    __tablename__ = 'communities'
    community_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    community_name = db.Column(db.String(20))
    description = db.Column(db.String(256))

    @staticmethod
    def get_all_communities():
        return Community.query.filter()

