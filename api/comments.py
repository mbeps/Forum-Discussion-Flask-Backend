
from flask import request, make_response, jsonify, Request, Response
from app import app, mycursor, mydb
from models import Comment


@app.route('/new_comment', methods=['POST'])
def new_comment() -> Response:
    """Creates a new comment for a post by a user.

    Fields:
        post_id (int)
        user_id (int)
        comment (str)

    Returns:
        Response: whether the comment was created or not
    """    
    comm: dict = request.get_json() # get the comment from the request
    post_id: int = comm.get('post_id') # get the post id
    user_id: int = comm.get('user_id') # get the user id
    comment: str = comm.get('comment') # get the comment
    
    cs: Comment = Comment(post_id=post_id, user_id=user_id, comment=comment) # create a comment object
    cs.save() # save the comment to the database
    return make_response(jsonify({'msg': 'Comment Added'}), 200) # return a response


@app.route('/all_comments', methods=['POST'])
def get_all_comments() -> Response:
    """Gets all the comments for a post.

    Fields:
        post_id (int)
        
    Returns:
        Response: all the comments for a post
    """    
    post: dict = request.get_json() # get the post from the request
    post_id: int = post.get('post_id') # get the post id
    
    mycursor.execute('''
        select u.username, c.comment, c.create_dttm from comments c join user u
        on u.user_id = c.user_id
        where c.post_id = %s
        ''', (post_id,)) # get all the comments for the post
    comments = mycursor.fetchall() # fetch all the comments
    mydb.commit() # commit the changes
    all_comments: list[dict] = []
    for comment in comments: # loop through the comments
        all_comments.append({ 
            'username': comment[0],
            'comment': comment[1],
            'comment_time': comment[2]
        }) # append the comment to the list
    return make_response(jsonify(all_comments), 200) # return all the comments


@app.route('/delete_comment', methods=['DELETE'])
def delete_comment() -> Response:
    """Deletes a comment for a post.

    Fields:
        comment_id (int)
        user_id (int)

    Returns:
        Response: whether the comment was deleted or not
    """    
    comm: dict = request.get_json() # get the comment from the request
    comment_id: int = comm.get('comment_id') # get the comment id
    user_id: int = comm.get('user_id') # get the user id
    
    comment: Comment = Comment.query.filter_by(comment_id=comment_id).first() # get the comment
    if comment: # if the comment exists
        if comment.user_id == user_id: # check if the user is the owner of the comment
            comment.delete_comment_by_id(comment_id) # delete the comment
            return make_response(jsonify({'msg': 'Comment Deleted'}), 200) # return a response
        return make_response(jsonify({'msg': 'You are not the owner of this comment'}), 400) # return a response
    return make_response(jsonify({'msg': 'Comment does not exist'}), 400) # return a response
