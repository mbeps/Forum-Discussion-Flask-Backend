from flask import make_response, jsonify, request, redirect, Request, Response
from sqlalchemy import text, engine

from app import app
from models import Community, CommunitySubscribe


@app.route('/add_community', methods=['POST'])
def add_community() -> Response:
    """Creates a new community. 
    The user who creates the community is automatically subscribed to it.

    Returns:
        Response: whether the community was created or not
    """    
    community = request.get_json() # get json data from request
    user_id: str = community.get('user_id') # get user_id from json data
    community_name: str = community.get('community_name') # get community_name from json data
    description: str = community.get('description') # get description from json data

    community: Community = Community(user_id=user_id, community_name=community_name, description=description) # create community object
    community.save() # save community object to database
    cs: CommunitySubscribe = CommunitySubscribe(user_id=user_id, community_id=community.community_id) # community creator is automatically subscribed to community
    cs.save() # save community subscribe object to database
    return make_response(jsonify({'msg': 'Community has been added'}), 200) # return success message


@app.route('/all_communities', methods=['GET'])
def get_all_communities():
    communities = Community.get_all_communities()
    communities_list = []
    for community in communities:
        communities_list.append({
            'community_id': community.community_id,
            'community_name': community.community_name,
            'description': community.description
        })
    return make_response(jsonify(communities_list), 200)