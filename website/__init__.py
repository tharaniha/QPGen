import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load config from .env
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')  # Use 'mysql' container name as host
    database = os.getenv('DB_NAME')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{username}:{password}@{host}/{database}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Uploads folder setup
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models after db initialization
    from .models import User, Subject, Question
    create_database(app)

    # Configure login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app


def create_database(app):
    with app.app_context():
        db.create_all()
        print('Database initialized!')

        # Create admin if not exists
        from .models import User
        admin_email = os.getenv('ADMIN_EMAIL')
        existing_admin = User.query.filter_by(email=admin_email).first()
        if not existing_admin:
            admin_user = User(
                firstname=os.getenv('ADMIN_NAME'),
                email=admin_email,
                password=generate_password_hash(os.getenv('ADMIN_PASSWORD'), method='pbkdf2:sha256'),
                designation="Administrator",
                department=os.getenv('ADMIN_DEPT'),
                experience=0,
                is_admin=True,
                is_mod=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user created with email: {admin_email}")
