from flask import make_response, jsonify, request, Request, Response
from sqlalchemy import text

from app import app, mycursor, mydb, db
from models import Post, LikePost, SavePost, CommunitySubscribe


@app.route('/create_post', methods=['POST'])
def create_post() -> Response:
    """Creates a post in a community.

    Fields:
        user_id (int)
        community_id (int)
        post_name (str)
        description (str)

    Returns:
        Response: whether the post was created or not
    """    
    post_data: dict = request.get_json() # get the post data
    user_id: int = post_data.get('user_id') # get the user id
    community_id: int = post_data.get('community_id') # get the community id
    post_name: str = post_data.get('post_name') # get the post name
    description: str = post_data.get('description') # get the description
    
    post: Post = Post(user_id=user_id, community_id=community_id, post_name=post_name, description=description) # create a post instance using the above data
    post.save() # save the post to the database

    return make_response(jsonify({'msg': 'post has been created'}), 200) # return a response to the user


@app.route('/remove_post', methods=['DELETE'])
def remove_post() -> Response:
    """Remove a post.

    Returns:
        Response: whether the post was removed or not
    """    
    post_data: dict = request.get_json()
    post_id: int = post_data.get('post_id')
    user_id: int = post_data.get('user_id')
    post: Post = Post.query.filter_by(post_id=post_id).first() # get the post
    if post.user_id == user_id: # check if the user is the owner of the post
        post.delete_post(post_id) # delete the post
        return make_response(jsonify({'msg': 'post has been removed'}), 200)
    return make_response(jsonify({'msg': 'you are not the owner of this post'}), 400)


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
    
    Fields:
        user_id (int)

    Returns:
        Response: all posts from all communities the user is subscribed to
    """    
    user: dict = request.get_json() # get the user data
    user_id: int = user.get('user_id') # get the user id
    
    posts: list = all_subscribed_community_posts(user_id) # get all posts from all communities the user is subscribed to
    all_posts: list[dict] = [] # create an empty list to store all posts
    for post in posts: # loop through all posts
        likes: LikePost = LikePost.query.filter(LikePost.post_id == post[0]).count() # get the number of likes for the post
        is_subscribed: CommunitySubscribe = CommunitySubscribe.query.filter_by(community_id=post[6], user_id=user_id).first() # check if the user is subscribed to the community
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

    Fields:
        user_id (int)
        post_id (int)

    Returns:
        Response: whether the post was liked or not
    """    
    comm_subs: dict = request.get_json() # get the post data
    post_id: int = comm_subs.get('post_id') # get the post id
    user_id: int = comm_subs.get('user_id') # get the user id
    
    if (LikePost.query.filter_by(post_id=post_id, user_id=user_id).first()): # if the user has already liked the post
        return make_response(jsonify({'msg': 'Post already liked'}), 400) # return a response to the user
    cs: LikePost = LikePost(post_id=post_id, user_id=user_id) # create a LikePost instance
    cs.save() # save the LikePost instance to the database
    likes: LikePost = LikePost.query.filter_by(post_id=post_id).count() # get the number of likes for the post
    return make_response(jsonify({'msg': 'You liked this post', 'total_likes': likes}), 200) # return a response to the user


@app.route('/dislike_post', methods=['POST'])
def dislike_post() -> Response:
    """Dislikes a post. 
    If the user has not liked the post, then the counter is not decremented.

    Fields:
        user_id (int)
        post_id (int)

    Returns:
        Response: whether the post was disliked or not
    """    
    comm_subs: dict = request.get_json() # get the post data
    post_id: int = comm_subs.get('post_id') # get the post id
    user_id: int = comm_subs.get('user_id') # get the user id
    
    if (LikePost.query.filter_by(post_id=post_id, user_id=user_id).first()): # if the user has liked the post
        LikePost.query.filter_by(post_id=post_id, user_id=user_id).delete() # delete the LikePost instance from the database
        db.session.commit() # commit the changes to the database
        likes: LikePost = LikePost.query.filter_by(post_id=post_id).count() # get the number of likes for the post
        return make_response(jsonify({'msg': 'You disliked this post', 'total_likes': likes}), 200) # return a response to the user
    return make_response(jsonify({'msg': 'You have not liked this post'}), 400) # return a response to the user


@app.route('/save_post', methods=['POST'])
def save_post() -> Response:
    """Saves a post for later viewing.

    Fields:
        user_id (int) 
        post_id (int)

    Returns:
        Response: whether the post was saved or not
    """    
    save: dict = request.get_json() # get the post data
    post_id: int = save.get('post_id') # get the post id
    user_id: int = save.get('user_id') # get the user id
    
    if SavePost.query.filter_by(post_id=post_id, user_id=user_id).first(): # if the user has already saved the post
        return make_response(jsonify({'msg': 'Post already in saved list'}), 400) # return a response to the user that the post is already saved
    cs: SavePost = SavePost(post_id=post_id, user_id=user_id) # create a SavePost instance
    cs.save() # save the SavePost instance to the database
    return make_response(jsonify({'msg': 'You saved this post'}), 200) # return a response to the user that the post was saved


def all_saved_posts(user_id: int) -> list:
    """Get all posts saved by the user.

    Args:
        user_id (int): user for which to get all saved posts

    Returns:
        list: list of all saved posts
    """    
    mycursor.execute('''
    select cp.post_id, cp.post_name, cp.description, u.username, c.community_name, cp.create_dttm from posts cp join user u
    on u.user_id = cp.user_id
    join community_subscribe cs
    on cs.community_id = cp.community_id
    join communities c on c.community_id = cp.community_id
    join save_post sp on sp.post_id = cp.post_id
    where sp.user_id = %s
    ''', (user_id,)) # get all posts from all communities the user is subscribed to
    data = mycursor.fetchall() # get all the data
    mydb.commit() # commit the changes to the database
    return data # return the data


@app.route('/all_saved_posts', methods=['POST'])
def get_all_saved_posts() -> Response:
    """Gets all posts saved by the user.

    Fields:
        user_id (int)
        
    Returns:
        Response: list of all posts saved by the user
    """
    user: dict = request.get_json() # get the user data
    user_id: int = user.get('user_id') # get the user id
    
    posts: int = all_saved_posts(user_id) # get all posts saved by the user
    all_posts: list[dict] = [] # create an empty list to store all posts
    for post in posts: # loop through all posts
        likes: LikePost = LikePost.query.filter(LikePost.post_id == post[0]).count() # get the number of likes for the post
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