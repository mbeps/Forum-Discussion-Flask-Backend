
from flask import request, make_response, jsonify, Request, Response
from app import app, mycursor, mydb
from models import Comment


@app.route('/new_comment', methods=['POST'])
def new_comment() -> Response:
    """Creates a new comment for a post by a user.

    Returns:
        Response: whether the comment was created or not
    """    
    comm = request.get_json() # get the comment from the request
    post_id: int = comm.get('post_id') # get the post id
    user_id: int = comm.get('user_id') # get the user id
    comment: str = comm.get('comment') # get the comment
    cs = Comment(post_id=post_id, user_id=user_id, comment=comment) # create a comment object
    cs.save() # save the comment to the database
    return make_response(jsonify({'msg': 'Comment Added'}), 200) # return a response




