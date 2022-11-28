from flask import make_response, jsonify, request, redirect
from sqlalchemy import text, engine

from app import app
from models import Community, CommunitySubscribe


@app.route('/add_community', methods=['POST'])
def add_community():
    community = request.get_json()
    user_id = community.get('user_id')
    community_name = community.get('community_name')
    description = community.get('description')

    community = Community(user_id=user_id, community_name=community_name, description=description)
    community.save()
    cs = CommunitySubscribe(user_id=user_id, community_id=community.community_id)
    cs.save()

    return make_response(jsonify({'msg': 'Community has been added'}), 200)


