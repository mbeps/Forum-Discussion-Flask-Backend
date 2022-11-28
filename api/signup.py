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



def email_authentication_code(email, user):
    msg = Message('Email Authentication', sender=app.config['MAIL_USERNAME'], recipients=[email])
    code = random.randint(100000, 999999)
    user.code = code
    user.save()
    msg.body = f"Code for email authentication is {code}"
    mail.send(msg)
    return "Sent"
