from flask import request, make_response, jsonify
from flask_mail import Message
from passlib.hash import pbkdf2_sha256
import random

from app import app, mail
from models import User


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_user = request.get_json()
    name = signup_user.get('username')
    email = signup_user.get('email')
    password = signup_user.get('password')
    password = pbkdf2_sha256.hash(password)

    if User.query.filter_by(email=email).all():
        return make_response(jsonify({'error': 'User already exist'}), 400)
    user = User(username=name, email=email, password=password)
    user.save()
    email_authentication_code(email, user)
    return make_response(jsonify({'msg': 'signed up success'}), 200)

@app.route('/verify_code', methods=['GET', 'POST'])
def signup_full():
    verify_mail = request.get_json() # Get the user data from the request
    code = verify_mail.get('code') # Get the code
    email = verify_mail.get('email') # Get the email
    user = User.query.filter_by(email=email).first() # Get the user from the database
    if user: # Check if the user exists
        if code == user.code: # Check if the code is correct
            user.is_authenticated = True # Set the user to authenticated
            user.save() # Save the user to the database
            return make_response(jsonify({'msg': 'Auth Success'}), 200) # Return success message
        return make_response(jsonify({'msg': 'Please enter correct code'}), 401) # Return error message if the code is incorrect
    return make_response(jsonify({'msg': 'No such user exist with this email'}), 200) # Return error message if the user does not exist


def email_authentication_code(email, user):
    msg = Message('Email Authentication', sender=app.config['MAIL_USERNAME'], recipients=[email])
    code = random.randint(100000, 999999)
    user.code = code
    user.save()
    msg.body = f"Code for email authentication is {code}"
    mail.send(msg)
    return "Sent"
