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
def get_all_communities() -> Response:
    """Gets all communities in the database. 

    Returns:
        Response: list of all communities
    """    
    communities = Community.get_all_communities() # get all communities from database
    communities_list: list[dict[str]] = [] # create empty list to store communities
    for community in communities:
        communities_list.append({ # append community to list
            'community_id': community.community_id,
            'community_name': community.community_name,
            'description': community.description
        })
    return make_response(jsonify(communities_list), 200) # return list of communities


@app.route('/all_communities/<int:user_id>', methods=['GET'])
def get_user_communities(user_id: int) -> Response:
    """Gets all communities that a user is subscribed to.

    Args:
        user_id (int): user for which to get communities

    Returns:
        Response: list of communities that user is subscribed to
    """    
    communities: CommunitySubscribe = CommunitySubscribe.get_all_subscribed_communities(user_id) # get all communities user is subscribed to
    communities_list: list[dict[str]] = [] # create empty list to store communities
    for community in communities: # append community to list
        communities_list.append({ 
            'community_id': community.community_id,
            'community_name': community.community_name,
            'description': community.description
        })
    return make_response(jsonify(communities_list), 200) # return list of communities


@app.route('/subscribe-community', methods=['POST'])
def subscribe_community() -> Response:
    """Allows a user to subscribe to a community.

    Returns:
        Response: whether the user was subscribed to the community or not
    """    
    comm_subs = request.get_json() # get json data from request
    community_id: int = comm_subs.get('community_id') # get community_id from json data
    user_id: int = comm_subs.get('user_id') # get user_id from json data
    if (CommunitySubscribe.query.filter_by(community_id=community_id, user_id=user_id).first()): # check if user is already subscribed to community:
        return make_response(jsonify({'msg': 'Community already subscribed'}), 400) # return error message if user is already subscribed to community
    cs: CommunitySubscribe = CommunitySubscribe(community_id=community_id, user_id=user_id) # create community subscribe object
    cs.save() # save community subscribe object to database
    return make_response(jsonify({'msg': 'Community Added'}), 200) # return success message


@app.route('/subscribed-community', methods=['POST'])
def all_subscribed_communities() -> Response:
    """Gets all communities that a user is subscribed to.

    Returns:
        Response: list of communities that user is subscribed to
    """    
    user = request.get_json() # get json data from request
    user_id: int = user.get('user_id') # get user_id from json data
    communities: Community = CommunitySubscribe.get_all_subscribed_communities(user_id) # get all communities user is subscribed to
    all_communities: list[dict] = [] # create empty list to store communities
    for community in communities:
       all_communities.append({ # append community to list
           'community_id': community.community_id,
           'community_name': community.community_name
       })
    return make_response(jsonify(all_communities), 200) # return list of communities


@app.route('/remove_community', methods=['DELETE'])
def remove_community() -> Response:
    """Deletes a community from the database.
    """
    community = request.get_json() # get json data from request
    community_id: int = community.get('community_id') # get community_id from json data
    if (Community.query.filter_by(community_id=community_id).first()):
        Community.delete_community(community_id) # delete community from database
        return make_response(jsonify({'msg': 'Community has been deleted'}), 200) # return success message
    return make_response(jsonify({'msg': 'Community does not exist'}), 400) # return error message if community does not exist


# unsubscribe from community given community_id and user_id
@app.route('/unsubscribe_community', methods=['DELETE'])
def unsubscribe_community() -> Response:
    """Unsubscribes a user from a community.

    Returns:
        Response: whether the user was unsubscribed from the community or not
    """    
    comm_subs = request.get_json() # get json data from request
    community_id: int = comm_subs.get('community_id') # get community_id from json data
    user_id: int = comm_subs.get('user_id') # get user_id from json data
    if (CommunitySubscribe.query.filter_by(community_id=community_id, user_id=user_id).first()): # check if user is subscribed to community
        CommunitySubscribe.unsubscribe_from_community(community_id, user_id) # unsubscribe user from community
        return make_response(jsonify({'msg': 'Community Unsubscribed'}), 200) # return success message
    return make_response(jsonify({'msg': 'Community not subscribed'}), 400) # return error message if user is not subscribed to community