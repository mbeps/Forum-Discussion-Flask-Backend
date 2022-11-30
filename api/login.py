from flask import request, make_response, jsonify, Response, Request
from passlib.hash import pbkdf2_sha256

from app import app
from models import User


@app.route('/login', methods=['POST'])
def login() -> Response:
    login_cred: Request = request.get_json() # Get the user data from the request
    email: str = login_cred.get('email') # Get the email
    password: str = login_cred.get('password') # Get the password 

    user: User = User.query.filter_by(email=email).first() # Get the user from the database
    if user: # Check if the user exists
        if pbkdf2_sha256.verify(password, user.password): # Check if the password is correct
            return make_response(jsonify( # Return success message with the user data
                {
                    'user_id': user.user_id,
                    'email': user.email,
                    'username': user.username,
                    'is_authenticated': user.is_authenticated
                }), 200)
    return make_response(jsonify({'error': 'Invalid credentials'}), 400) # Return error message if the user does not exist or the password is incorrect
