from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_mail import Mail
from environs import Env
from flask_cors import CORS
import pymysql
import mysql.connector

env = Env()
env.read_env()

app = Flask(__name__)

database_user: str = env.str('USER')
database_password: str = env.str('PASSWORD')
database_name: str = env.str('DATABASE')

CORS(app)
app.secret_key = 'abc123'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{database_user}:{database_password}@localhost:3306/{database_name}'

pymysql.install_as_MySQLdb()

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = env.str('EMAIL')
app.config['MAIL_PASSWORD'] = env.str('SECRET')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False

mail = Mail(app)
db = SQLAlchemy(app)

from models import *

with app.app_context():
    db.create_all()

mydb = mysql.connector.connect(
  host=env.str('HOST'),
  user=env.str('USER'),
  password=env.str('PASSWORD'),
  database=env.str('DATABASE')
)
mycursor = mydb.cursor()


from api.signup import *
from api.login import *
from api.community import *
from api.create_post import *
from api.comments import *