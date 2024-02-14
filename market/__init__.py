# Flask APP initialisation. Our Python package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'c907f561cdcc92023d1ea3ef'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# specifies to the login manager where login page is located, to use login_required
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from market import routes