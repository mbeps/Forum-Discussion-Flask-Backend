from flask import request, make_response, jsonify, Response
from flask_mail import Message
from passlib.hash import pbkdf2_sha256
import random

from app import app, mail
from models import User


@app.route('/signup', methods=['GET', 'POST'])
def signup() -> Response:
    """Allows user to sign up.
    If the already exists, it will return an error informing the user that the email is already in use.
    If the email does not exist, it will create a new user and send an email with a code to authenticate the email.

    Fields:
        username (str)
        email (str)
        password (str)

    Returns:
        Response: status of signup (success or error)
    """
    signup_user: dict = request.get_json() # Get the user data from the request
    name: str = signup_user.get('username') # Get the username
    email: str = signup_user.get('email') # Get the email
    password: str = signup_user.get('password') # Get the password
    password: str = pbkdf2_sha256.hash(password) # Hash the password

    if User.query.filter_by(email=email).all(): # Check if the email already exists
        return make_response(jsonify({'error': 'User already exist'}), 400) # Return error if the email already exists
    # if user does not exist, create a new user
    user: User = User(username=name, email=email, password=password) # Create a new user
    user.save() # Save the user to the database
    email_authentication_code(email, user) # Send the email authentication code
    return make_response(jsonify({'msg': 'signed up success'}), 200) # Return success message


@app.route('/verify_code', methods=['GET', 'POST'])
def signup_full() -> Response:
    """Completes signup by verifying the code sent to the email.
    Authenticates user who has tried to sign up.
    If the code is correct, it will return a success message and the user will be able to log in.

    Fields:
        email (str)
        code (int)

    Returns:
        Response: whether the signup was successful or not
    """    
    verify_mail: dict = request.get_json() # Get the user data from the request
    code: int = verify_mail.get('code') # Get the code
    email: str = verify_mail.get('email') # Get the email
    user: User = User.query.filter_by(email=email).first() # Get the user from the database
    if user: # Check if the user exists
        if code == user.code: # Check if the code is correct
            user.is_authenticated: bool = True # Set the user to authenticated
            user.save() # Save the user to the database
            return make_response(jsonify({'msg': 'Auth Success'}), 200) # Return success message
        return make_response(jsonify({'msg': 'Please enter correct code'}), 401) # Return error message if the code is incorrect
    return make_response(jsonify({'msg': 'No such user exist with this email'}), 200) # Return error message if the user does not exist


def email_authentication_code(email, user) -> str:
    """Authenticates the email by sending a code to the email.

    Args:
        email (str): email to send the code to and authenticate
        user (str): user to get the code from

    Returns:
        str: Message sent to the email
    """    
    msg: Message = Message('Email Authentication', sender=app.config['MAIL_USERNAME'], recipients=[email]) # Create the email message
    code: int = random.randint(100000, 999999) # Generate a random code
    user.code = code # Set the code to the user
    user.save() # Save the user to the database
    msg.body: str = f"Code for email authentication is {code}" # Set the body of the email
    mail.send(msg) # Send the email
    return "Sent" # Return success message