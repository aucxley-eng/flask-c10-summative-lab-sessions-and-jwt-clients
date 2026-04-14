from app.models import db, User, generate_api_key
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
    
    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def find_by_username(self, username):
        return User.query.filter_by(username=username).first()
    
    def find_by_api_key(self, api_key):
        return User.query.filter_by(api_key=api_key).first()
    
    def create_with_api_key(self, username, email, password):
        user = User(
            username=username,
            email=email,
            api_key=generate_api_key()
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    def generate_new_api_key(self, user):
        user.api_key = generate_api_key()
        db.session.commit()
        return user