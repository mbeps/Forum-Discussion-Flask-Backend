import pytest
from app import app
from models import User, Community, CommunitySubscribe, Post



def test_create_post(client):
    # create a post
    response = client.post('/create_post', json={
        'user_id': 1,
        'community_id': 2,
        'post_name': 'Test post',
        'description': 'This is a test post.'
    })

    # assert that the response has a success status code
    assert response.status_code == 200

    # assert that the response contains the correct message
    assert response.json == {'msg': 'post has been created'}

def test_remove_post(client):
    # create a post
    response = client.post('/create_post', json={
        'user_id': 1,
        'community_id': 2,
        'post_name': 'Test post',
        'description': 'This is a test post.'
    })

    # get the post data
    post_data = response.json

    # remove the post
    response = client.delete('/remove_post', json={
        'post_id': post_data['post_id'],
        'user_id': post_data['user_id']
    })

    # assert that the response has a success status code
    assert response.status_code == 200

    # assert that the response contains the correct message
    assert response.json == {'msg': 'post has been removed'}

def test_get_all_posts(client):
    # create a post
    response = client.post('/create_post', json={
        'user_id': 1,
        'community_id': 2,
        'post_name': 'Test post',
        'description': 'This is a test post.'
    })

    # get the post data
    post_data = response.json

    # get all posts
    response = client.post('/all_posts', json={
        'user_id': post_data['user_id']
    })

    # assert that the response has a success status code
    assert response.status_code == 200

    # assert that the response contains the post data
    assert post_data in response.json
