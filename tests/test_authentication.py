import pytest
from app import app
from models import User
import tests

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_signup(client):
    # Test successful signup
    signup_data = {'username': 'test_user', 'email': 'test_user@gmail.com', 'password': 'test_password'}
    response = client.post('/signup', json=signup_data)
    assert response.status_code == 200
    assert response.json['msg'] == 'signed up success'

    # Test signup with already existing email
    signup_data = {'username': 'test_user', 'email': 'test_user@gmail.com', 'password': 'test_password'}
    response = client.post('/signup', json=signup_data)
    assert response.status_code == 400
    assert response.json['error'] == 'User already exist'

def test_verify_code(client):
    # Test successful code verification
    signup_data = {'username': 'test_user', 'email': 'test_user@gmail.com', 'password': 'test_password'}
    client.post('/signup', json=signup_data)

    user = User.query.filter_by(email='test_user@gmail.com').first()
    verify_data = {'email': 'test_user@gmail.com', 'code': user.code}
    response = client.post('/verify_code', json=verify_data)
    assert response.status_code == 200
    assert response.json['msg'] == 'Auth Success'

    # Test incorrect code verification
    signup_data = {'username': 'test_user', 'email': 'test_user@gmail.com', 'password': 'test_password'}
    client.post('/signup', json=signup_data)

    user = User.query.filter_by(email='test_user@gmail.com').first()
    verify_data = {'email': 'test_user@gmail.com', 'code': user.code + 1}
    response = client.post('/verify_code', json=verify_data)
    assert response.status_code == 401
    assert response.json['msg'] == 'Please enter correct code'

def test_login(client):
    # Test successful login
    signup_data = {'username': 'test_user', 'email': 'test_user@gmail.com', 'password': 'test_password'}
    client.post('/signup', json=signup_data)
    user = User.query.filter_by(email='test_user@gmail.com').first()
    verify_data = {'email': 'test_user@gmail.com', 'code': user.code}
    client.post('/verify_code', json=verify_data)

    login_data = {'email': 'test_user@gmail.com', 'password': 'test_password'}
    response = client.post('/login', json=login_data)
    assert response.status_code == 200
    assert response.json['username'] == 'test_user'
    assert response.json['email'] == 'test_user@gmail.com'
    assert response.json['is_authenticated'] == True

	# Test login with incorrect credentials
    login_data = {'email': 'test_user@gmail.com', 'password': 'incorrect_password'}
    response = client.post('/login', json=login_data)
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid credentials'

def test_login_unauthenticated_user(client):
    # Test login with unauthenticated user
    signup_data = {'username': 'test_user', 'email': 'test_user@gmail.com', 'password': 'test_password'}
    client.post('/signup', json=signup_data)
    login_data = {'email': 'test_user@gmail.com', 'password': 'test_password'}
    response = client.post('/login', json=login_data)
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid credentials'
