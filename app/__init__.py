from flask import Flask, g, request, make_response
from flask_login import LoginManager
from mongoengine import disconnect
from .models import db, User
from config import Config
from .api import api as api_blueprint
from .auth import auth as auth_blueprint
from flask_cors import CORS
from .cli import init_cli
import time

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.objects(id=user_id).first()
    except:
        return None


def create_app(config_class=Config):
    print("Initializing Flask application...")
    app = Flask(__name__)
    app.config.from_object(config_class)

    print("Initializing database...")
    try:
        disconnect()
        db.init_app(app)
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

    print("Initializing login manager...")
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    print("Registering blueprints...")
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")
    app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")
    allowed_origins = ["http://localhost:5173", "https://cursor.beauty", "https://www.cursor.beauty"]

    # 初始化 CORS，添加更多配置
    CORS(
        app,
        origins=allowed_origins,
        allow_credentials=True,
        supports_credentials=True,
        resources={
            r"/api/*": {
                "origins": allowed_origins,
                "allow_headers": ["Content-Type", "Authorization"],
                "expose_headers": ["Content-Type", "Authorization"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "max_age": 3600,
            }
        },
    )

    # 添加请求超时处理
    @app.before_request
    def handle_timeout():
        g.request_start_time = time.time()
        g.request_timeout = False

    @app.after_request
    def add_cors_headers(response):
        allowed_origins = [
            "http://localhost:5173",
            "https://cursor.beauty",
            "https://www.cursor.beauty"
        ]
        
        origin = request.headers.get('Origin')
        
        # 如果请求来自允许的域名，则设置对应的单个 origin
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
            response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
        
        return response

    # 初始化命令行工具
    init_cli(app)

    print("Flask application initialized successfully")
    return app
