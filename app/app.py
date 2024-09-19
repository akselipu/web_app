from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from config import Config


app = Flask(__name__)
app.secret_key = "abc1234567890" 
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://leopuustinen:aksu@localhost:5432/postgres"
#app.config.from_object(Config)

# Import your routes after initializing the app and db
import routes
