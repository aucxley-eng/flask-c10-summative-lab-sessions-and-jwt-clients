import re
from app.repositories import UserRepository


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    def validate_email(self, email):
        pattern = r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'
        return re.match(pattern, email)
    
    def validate_registration_data(self, data):
        errors = []
        required_fields = ['username', 'email', 'password']
        
        for field in required_fields:
            if not data.get(field):
                errors.append(field)
        
        if errors:
            return False, f'Missing required fields: {errors}'
        
        if not self.validate_email(data.get('email', '')):
            return False, 'Invalid email format'
        
        if len(data.get('password', '')) < 6:
            return False, 'Password must be at least 6 characters'
        
        return True, None
    
    def register(self, data):
        is_valid, error = self.validate_registration_data(data)
        if not is_valid:
            return None, error
        
        if self.user_repo.find_by_username(data['username']):
            return None, f'Username {data['username']} already exists'
        
        if self.user_repo.find_by_email(data['email']):
            return None, f'Email {data['email']} already registered'
        
        try:
            user = self.user_repo.create_with_api_key(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            return user, None
        except Exception as e:
            return None, 'Error creating user'
    
    def login(self, email, password):
        if not email or not password:
            return None, 'Email and password required'
        
        user = self.user_repo.find_by_email(email)
        
        if not user:
            return None, 'Invalid email or password'
        
        if not user.check_password(password):
            return None, 'Invalid email or password'
        
        if not user.api_key:
            user = self.user_repo.generate_new_api_key(user)
        
        return user, None
    
    def get_user_by_api_key(self, api_key):
        return self.user_repo.find_by_api_key(api_key)
    
    def refresh_api_key(self, user):
        return self.user_repo.generate_new_api_key(user)