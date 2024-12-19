from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_caching import Cache
import os

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()
migrate = Migrate()  # Initialize Migrate
cache = Cache()  # Initialize Cache without config


def create_app():
    app = Flask(__name__)

    # Load configuration
    from .config import Config
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Link Migrate with app and db
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)  # Initialize cache with app

    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        create_default_admin()

    return app


def create_default_admin():
    from app.models import User
    admin_email = 'email@admin.com'
    admin_username = 'admin'
    admin_password = 'password'

    if not User.query.filter_by(email=admin_email).first():
        hashed_password = bcrypt.generate_password_hash(
            admin_password).decode('utf-8')
        admin = User(username=admin_username, email=admin_email,
                     password=hashed_password, is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print('Default admin account created.')


# Instantiate the app
app = create_app()
