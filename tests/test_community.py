import pytest
from app import app
from models import User, Community, CommunitySubscribe
from models.post import Post

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_add_community(client):
    # Test successful addition of community
    user = User(username='test_user', email='test_user@gmail.com', password='test_password')
    user.save()
    add_community_data = {'user_id': user.user_id, 'community_name': 'test_community', 'description': 'test_description'}
    response = client.post('/add_community', json=add_community_data)
    assert response.status_code == 200
    assert response.json['msg'] == 'Community has been added'

def test_get_all_communities(client):
    # Test getting all communities
    user = User(username='test_user', email='test_user@gmail.com', password='test_password')
    user.save()
    community = Community(user_id=user.user_id, community_name='test_community', description='test_description')
    community.save()
    response = client.get('/all_communities')
    assert response.status_code == 200
    assert response.json[0]['community_name'] == 'test_community'
    assert response.json[0]['description'] == 'test_description'

def test_get_user_communities(client):
    # Test getting all communities that a user is subscribed to
    user = User(username='test_user', email='test_user@gmail.com', password='test_password')
    user.save()
    community = Community(user_id=user.user_id, community_name='test_community', description='test_description')
    community.save()
    community_sub = CommunitySubscribe(user_id=user.user_id, community_id=community.community_id)
    community_sub.save()
    response = client.get('/all_communities/' + str(user.user_id))
    assert response.status_code == 200
    assert response.json[0]['community_name'] == 'test_community'
    assert response.json[0]['description'] == 'test_description'

def test_subscribe_community(client):
    # Test successful subscription to a community
    user = User(username='test_user', email='test_user@gmail.com', password='test_password')
    user.save()
    community = Community(user_id=user.user_id, community_name='test_community', description='test_description')
    community.save()
    subscribe_community_data = {'community_id': community.community_id, 'user_id': user.user_id}
    response = client.post('/subscribe-community', json=subscribe_community_data)
    assert response.status_code == 200
    assert response.json['msg'] == 'Community Added'

def test_subscribe_to_already_subscribed_community(client):
    # Test subscribing to a community that user is already subscribed to
    user = User(username='test_user', email='test_user@gmail.com', password='test_password')
    user.save()
    community = Community(user_id=user.user_id, community_name='test_community', description='test_description')
    community.save()
    community_sub = CommunitySubscribe(user_id=user.user_id, community_id=community.community_id)
    community_sub.save()
    subscribe_community_data = {'community_id': community.community_id, 'user_id': user.user_id}
    response = client.post('/subscribe-community', json=subscribe_community_data)
    assert response.status_code == 400
    assert response.json['msg'] == 'Community already subscribed'

def test_add_post(client):
    # Test successful addition of a post
    user = User(username='test_user', email='test_user@gmail.com', password='test_password')
    user.save()
    community = Community(user_id=user.user_id, community_name='test_community', description='test_description')
    community.save()
    add_post_data = {'user_id': user.user_id, 'community_id': community.community_id, 'text': 'test_text'}
    response = client.post('/add_post', json=add_post_data)
    assert response.status_code == 200
    assert response.json['msg'] == 'Post added'

def test_get_all_posts(client):
    # Test getting all posts from all communities
    user = User(username='test_user', email='test_user@gmail.com', password='test_password')
    user.save()
    community = Community(user_id=user.user_id, community_name='test_community', description='test_description')
    community.save()
    post = Post(user_id=user.user_id, community_id=community.community_id, text='test_text')
    post.save()
    response = client.get('/all_posts')
    assert response.status_code == 200
    assert response.json[0]['text'] == 'test_text'

def test_get_community_posts(client):
    # Test getting all posts from a specific community
    user = User(username='test_user', email='test_user@gmail.com', password='test_password')
    user.save()
    community = Community(user_id=user.user_id, community_name='test_community', description='test_description 1')
    community.save()
    community2 = Community(user_id=user.user_id, community_name='test_community2', description='test_description 2')
    community2.save()
    post = Post(user_id=user.user_id, community_id=community.community_id, text='test_text')
    post.save()
    post2 = Post(user_id=user.user_id, community_id=community2.community_id, text='test_text')
    post2.save()   
    response = client.get('/all_posts/' + str(community.community_id))
    assert response.status_code == 200
    assert response.json[0]['text'] == 'test_text'


