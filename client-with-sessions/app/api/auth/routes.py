from flask import Blueprint, request, session, jsonify
from app.services import AuthService
from app.schemas import UserSchema
from app.responses import APIResponse

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()


@auth_bp.route('/signup', methods=['POST'])
def register():
    data = request.get_json() or {}
    
    auth_service = AuthService()
    user, error = auth_service.register(data)
    
    if error:
        if 'already exists' in error.lower():
            return APIResponse.conflict(error)
        return APIResponse.error(error, 'Validation Error', 400)
    
    # Session-based
    session['user_id'] = user.id
    
    return APIResponse.success(
        data={
            'user': user_schema.dump(user)
        },
        message='User registered successfully',
        status_code=201
    )


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    
    auth_service = AuthService()
    user, error = auth_service.login(username, password)
    
    if error:
        return APIResponse.unauthorized(error)
    
    # Session-based
    session['user_id'] = user.id
    
    return APIResponse.success(
        data={
            'user': user_schema.dump(user)
        },
        message='Login successful'
    )


@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    
    if not user_id:
        return APIResponse.success(data={})
    
    auth_service = AuthService()
    user = auth_service.get_user_by_id(user_id)
    
    if not user:
        return APIResponse.success(data={})
    
    return APIResponse.success(data={'user': user_schema.dump(user)})


@auth_bp.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return APIResponse.success(message='Logged out successfully')