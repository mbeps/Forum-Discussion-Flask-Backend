from flask import make_response, jsonify, request, Request, Response
from sqlalchemy import text

from app import app, mycursor, mydb, db
from models import Post, LikePost, SavePost, CommunitySubscribe


@app.route('/create_post', methods=['POST'])
def create_post() -> Response:
    """Creates a post in a community

    Returns:
        Response: whether the post was created or not
    """    
    post_data = request.get_json() # get the post data
    user_id: int = post_data.get('user_id') # get the user id
    community_id: int = post_data.get('community_id') # get the community id
    post_name: str = post_data.get('post_name') # get the post name
    description: str = post_data.get('description') # get the description
    post = Post(user_id=user_id, community_id=community_id, post_name=post_name, description=description) # create a post instance using the above data
    post.save() # save the post to the database

    return make_response(jsonify({'msg': 'post has been created'}), 200) # return a response to the user