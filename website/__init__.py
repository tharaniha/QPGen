import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
db = SQLAlchemy()
migrate = Migrate()  # Add this
DB_NAME = "qpdatabase.db"

# Database connection info (using environment variables for better security)
username = os.getenv('DB_USERNAME', 'root')
password = os.getenv('DB_PASSWORD', 'Tharan%402004')
host = os.getenv('DB_HOST', 'localhost')
database = os.getenv('DB_NAME', 'qpdatabase')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'defaultsecretkey')  # Better to keep secrets in environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@{host}/{database}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary Flask-SQLAlchemy modification tracking

    # Initialize db and migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Correctly reference the 'uploads' folder located outside 'website'
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')

    # Get the absolute path for the 'uploads' folder located outside 'website'
    upload_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))

    # Print the resolved absolute path
    print("Upload folder path:", upload_folder_path)

    # Check if the directory exists
    if os.path.exists(upload_folder_path):
        print("Uploads folder exists.")
    else:
        print("Uploads folder does NOT exist.")

    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit, adjust as needed

    # Ensure the uploads folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    migrate.init_app(app, db)

    # Import and register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models after db initialization
    from .models import User, Subject, Question

    # Create database if it doesn't exist and add admin
    create_database(app)

    # Configure Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = None  # Disable the default "Please log in to access this page" message
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    db_path = path.join('website', DB_NAME)
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
            print('Created Database!')

            # Add an admin user if not already present
            from .models import User
            admin_email = "admin@gmail.com"
            pd = generate_password_hash("admin123", method='pbkdf2:sha256')
            existing_admin = User.query.filter_by(email=admin_email).first()
            if not existing_admin:
                admin_user = User(                    
                    firstname="Admin",
                    email=admin_email,
                    password=pd,
                    designation="Administrator",  # Default designation
                    department="Administration",  # Default department
                    experience=0,                  # Default experience                    
                    is_admin=True,
                    is_mod=True
                )
                db.session.add(admin_user)
                db.session.commit()
                print("Admin user created with email:", admin_email)
    else:
        print("Database already exists.")

