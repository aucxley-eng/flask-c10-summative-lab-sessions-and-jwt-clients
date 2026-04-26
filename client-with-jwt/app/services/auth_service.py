import re
from app.repositories import UserRepository


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    def validate_registration_data(self, data):
        errors = []
        required_fields = ['username', 'password']
        
        for field in required_fields:
            if not data.get(field):
                errors.append(field)
        
        if errors:
            return False, f'Missing required fields: {errors}'
        
        if len(data.get('password', '')) < 6:
            return False, 'Password must be at least 6 characters'
        
        if data.get('email') and not re.match(r"[^@]+@[^@]+\.[^@]+", data.get('email', '')):
            return False, 'Invalid email format'
        
        return True, None
    
    def register(self, data):
        is_valid, error = self.validate_registration_data(data)
        if not is_valid:
            return None, error
        
        if self.user_repo.find_by_username(data['username']):
            return None, f"Username {data['username']} already exists"
        
        try:
            user = self.user_repo.create_user(
                username=data['username'],
                password=data['password'],
                email=data.get('email')
            )
            return user, None
        except Exception as e:
            return None, 'Error creating user'
    
    def login(self, username, password):
        if not username or not password:
            return None, 'Username and password required'
        
        user = self.user_repo.find_by_username(username)
        
        if not user:
            return None, 'Invalid username or password'
        
        if not user.check_password(password):
            return None, 'Invalid username or password'
        
        return user, None
    
    def get_user_by_id(self, user_id):
        return self.user_repo.get_by_id(user_id)