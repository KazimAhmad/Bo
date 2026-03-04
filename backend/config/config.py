from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config.constants import databaseName, image_uploads, allowed_extensions

app = Flask(__name__)

app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png"]
app.config["UPLOAD_PATH"] = image_uploads

app.config["SQLALCHEMY_DATABASE_URI"] = databaseName
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)