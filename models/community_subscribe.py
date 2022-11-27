from sqlalchemy import text, engine

from app import db
from models import AppModel
from models.community import Community


class CommunitySubscribe(db.Model, AppModel):
    __tablename__ = 'community_subscribe'
    community_subscribe_id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)


