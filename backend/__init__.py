from flask import Flask

# Initialize the Flask application
app = Flask(__name__, static_url_path='', static_folder='../frontend')


# app.config['SECRET_KEY'] = 'your_secret_key'


from . import views


# from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-database.db'
# db = SQLAlchemy(app)

# You might have other initializations like for login manager, mail, etc.
