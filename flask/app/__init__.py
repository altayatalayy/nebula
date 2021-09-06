from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from app.config import ProdConfig, DevConfig, TestConfig
def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    db = SQLAlchemy(app)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'main.login'

    return app, db, bcrypt, login_manager

app, db, bcrypt, login_manager = create_app()
host, port = '10.0.3.159', 5000
host, port = '10.0.4.60', 5000
host, port = 'localhost', 5000
base_url = f'http://{host}:{port}'

from app.main.routes import main
#from app.apis.data import data
#from app.apis.auth import auth
app.register_blueprint(main)
#app.register_blueprint(data)
#app.register_blueprint(auth)
