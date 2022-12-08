import pytest
from app import app
from models import Comment

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_new_comment(client):
    pass

def test_get_all_comments(client):
    pass

def test_delete_comment(client):
    pass

def test_new_comment(client):
    # create a new comment
    data = {
        'post_id': 1,
        'user_id': 1,
        'comment': 'This is a new comment'
    }
    response = client.post('/new_comment', json=data)
    assert response.status_code == 200
    assert response.get_json() == {'msg': 'Comment Added'}

    # check that the comment was added to the database
    comment = Comment.query.filter_by(post_id=1, user_id=1).first()
    assert comment.comment == 'This is a new comment'

def test_get_all_comments(client):
    # create some comments for a post
    Comment(post_id=1, user_id=1, comment='Comment 1').save()
    Comment(post_id=1, user_id=2, comment='Comment 2').save()
    Comment(post_id=1, user_id=3, comment='Comment 3').save()

    # get all the comments for the post
    response = client.post('/all_comments', json={'post_id': 1})
    assert response.status_code == 200

    # check that all the comments are returned
    comments = response.get_json()
    assert len(comments) == 3
    assert comments[0]['username'] == 'user1'
    assert comments[0]['comment'] == 'Comment 1'
    assert comments[1]['username'] == 'user2'
    assert comments[1]['comment'] == 'Comment 2'
    assert comments[2]['username'] == 'user3'
    assert comments[2]['comment'] == 'Comment 3'

def test_delete_comment(client):
    # create a comment
    Comment(post_id=1, user_id=1, comment='Comment to be deleted').save()

    # delete the comment
    response = client.delete('/delete_comment', json={'comment_id': 1, 'user_id': 1})
    assert response.status_code == 200
    assert response.get_json() == {'msg': 'Comment Deleted'}

    # try to delete a comment that does not exist
    response = client.delete('/delete_comment', json={'comment_id': 2, 'user_id': 1})
    assert response.status_code == 400
    assert response.get_json() == {'msg': 'Comment does not exist'}

    # try to delete a comment that was created by another user
    Comment(post_id=1, user_id=2, comment='Comment by another user').save()
    response = client.delete('/delete_comment', json={'comment_id': 2, 'user_id': 1})
    assert response.status_code == 400
    assert response.get_json() == {'msg': 'You are not the owner of this comment'}
