from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']= "ea34283308ca600a82345b884d250ab3"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.index"
login_manager.login_message = "Login or Register"
login_manager.login_message_category = "warning"
from .authetication.routes import auth_bp
from .users.routes import users


# Registering blueprints for authentication and user management
app.register_blueprint(auth_bp)
app.register_blueprint(users)
#app.config['SECRET_KEY'] = 'your_secret_key_here'


