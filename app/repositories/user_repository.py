from app.models import db, User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
    
    def find_by_username(self, username):
        return User.query.filter_by(username=username).first()
    
    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def create_user(self, username, password):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user