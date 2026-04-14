from flask import Blueprint, request
from app.services import AuthService
from app.schemas import UserSchema
from app.utils.decorators import require_auth
from app.responses import APIResponse

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    
    auth_service = AuthService()
    user, error = auth_service.register(data)
    
    if error:
        if 'already exists' in error.lower() or 'already registered' in error.lower():
            return APIResponse.conflict(error)
        return APIResponse.error(error, 'Validation Error', 400)
    
    user_data = user_schema.dump(user)
    user_data['api_key'] = user.api_key
    
    return APIResponse.success(
        data={'user': user_data, 'api_key': user.api_key},
        message='User registered successfully',
        status_code=201
    )


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    
    auth_service = AuthService()
    user, error = auth_service.login(email, password)
    
    if error:
        return APIResponse.unauthorized(error)
    
    user_data = user_schema.dump(user)
    user_data['api_key'] = user.api_key
    
    return APIResponse.success(
        data={'api_key': user.api_key, 'user': user_data},
        message='Login successful'
    )


@auth_bp.route('/me', methods=['GET'])
@require_auth()
def get_current_user():
    user = request.current_user
    user_data = user_schema.dump(user)
    user_data['api_key'] = user.api_key
    return APIResponse.success(data=user_data)


@auth_bp.route('/refresh-key', methods=['POST'])
@require_auth()
def refresh_api_key():
    auth_service = AuthService()
    user = auth_service.refresh_api_key(request.current_user)
    
    return APIResponse.success(
        data={'api_key': user.api_key},
        message='API key refreshed successfully'
    )