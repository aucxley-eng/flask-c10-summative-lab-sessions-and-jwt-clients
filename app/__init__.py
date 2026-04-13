import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    from app.routes import auth_bp, notes_bp
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    
    with app.app_context():
        from app import models
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5555)