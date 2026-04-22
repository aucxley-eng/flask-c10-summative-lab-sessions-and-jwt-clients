from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from app.models import db, bcrypt

jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)
    
    from app.api import auth_bp, notes_bp
    
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error='Bad Request', message=str(e.description)), 400
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error='Not Found', message='Resource not found'), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify(error='Internal Server Error', message='An unexpected error occurred'), 500
    
    return app