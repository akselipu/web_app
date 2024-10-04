from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from os import getenv


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

# Import your routes after initializing the app and db
import routes
