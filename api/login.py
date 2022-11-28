from flask import request, make_response, jsonify
from passlib.hash import pbkdf2_sha256

from app import app
from models import User


@app.route('/login', methods=['POST'])
def login():
    login_cred = request.get_json()
    email = login_cred.get('email')
    password = login_cred.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        if pbkdf2_sha256.verify(password, user.password):
            return make_response(jsonify(
                {
                    'user_id': user.user_id,
                    'email': user.email,
                    'username': user.username,
                    'is_authenticated': user.is_authenticated
                }), 200)
    return make_response(jsonify({'error': 'Invalid credentials'}), 400)
