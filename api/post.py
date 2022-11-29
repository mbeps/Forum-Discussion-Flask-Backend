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


def all_subscribed_community_posts(user_id: int) -> list[dict[str]]:
    """Find all posts in communities that a user is subscribed to.

    Args:
        user_id (int): user for which to find posts

    Returns:
        list[dict[str]]: list of posts
    """    
    mycursor.execute('''
    select cp.post_id, cp.post_name, cp.description, u.username, c.community_name, cp.create_dttm, c.community_id from posts cp
    join user u on u.user_id = cp.user_id
    join communities c on c.community_id = cp.community_id
    order by cp.create_dttm desc
    -- where cp.user_id = %s
    ''') # get all posts from all communities the user is subscribed to
    # ''', (user_id,))
    data: list = mycursor.fetchall() # fetch all the data
    mydb.commit() # commit the changes to the database
    return data # return the data


@app.route('/all_posts', methods=['POST'])
def get_all_posts() -> Response:
    """Gets all posts from all communities the user is subscribed to along with other data. 
    Each post will have:
    - post_id
    - post_name
    - description
    - username
    - community_name
    - total_likes
    - posted_time

    Returns:
        Response: all posts from all communities the user is subscribed to
    """    
    user = request.get_json() # get the user data
    user_id: int = user.get('user_id') # get the user id
    posts: list = all_subscribed_community_posts(user_id) # get all posts from all communities the user is subscribed to
    all_posts: list[dict] = [] # create an empty list to store all posts
    for post in posts: # loop through all posts
        likes = LikePost.query.filter(LikePost.post_id == post[0]).count() # get the number of likes for the post
        is_subscribed = CommunitySubscribe.query.filter_by(community_id=post[6], user_id=user_id).first() # check if the user is subscribed to the community
        if is_subscribed: # if the user is subscribed to the community 
            all_posts.append({ 
                'post_id': post[0],
                'post_name': post[1],
                'description': post[2],
                'username': post[3],
                'community_name': post[4],
                "total_likes": likes,
                "posted_time": post[5]
            }) # append the post to the list of posts
    return make_response(jsonify(all_posts), 200) # return the list of posts to the user


@app.route('/like_post', methods=['POST'])
def like_post() -> Response:
    """Likes a post. 
    If the user has already liked the post, then the counter is not incremented.

    Returns:
        Response: whether the post was liked or not
    """    
    comm_subs = request.get_json() # get the post data
    post_id: int = comm_subs.get('post_id') # get the post id
    user_id: int = comm_subs.get('user_id') # get the user id
    if (LikePost.query.filter_by(post_id=post_id, user_id=user_id).first()): # if the user has already liked the post
        return make_response(jsonify({'msg': 'Post already liked'}), 400) # return a response to the user
    cs = LikePost(post_id=post_id, user_id=user_id) # create a LikePost instance
    cs.save() # save the LikePost instance to the database
    likes = LikePost.query.filter_by(post_id=post_id).count() # get the number of likes for the post
    return make_response(jsonify({'msg': 'You liked this post', 'total_likes': likes}), 200) # return a response to the user


@app.route('/dislike', methods=['POST'])
def dislike():
    comm_subs = request.get_json() # get the post data
    post_id: int = comm_subs.get('post_id') # get the post id
    user_id: int = comm_subs.get('user_id') # get the user id
    likes = LikePost.query.filter_by(post_id=post_id, user_id=user_id).delete() # delete the LikePost instance from the database
    db.session.commit() # commit the changes to the database
    likes = LikePost.query.filter_by(post_id=post_id).count() # get the number of likes for the post
    return make_response(jsonify({'msg': 'You dislike this post', 'total_likes': likes}), 200) # return a response to the user
