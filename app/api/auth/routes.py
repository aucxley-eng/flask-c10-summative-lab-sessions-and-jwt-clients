from flask import Blueprint, request, session, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
    
    # Session-based (keep for backward compatibility)
    session['user_id'] = user.id
    
    # JWT-based
    access_token = create_access_token(identity=str(user.id))
    
    return APIResponse.success(
        data={
            'user': user_schema.dump(user),
            'token': access_token
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
    
    # Session-based (keep for backward compatibility)
    session['user_id'] = user.id
    
    # JWT-based
    access_token = create_access_token(identity=str(user.id))
    
    return APIResponse.success(
        data={
            'user': user_schema.dump(user),
            'token': access_token
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


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    
    auth_service = AuthService()
    user = auth_service.get_user_by_id(user_id)
    
    if not user:
        return APIResponse.not_found('User not found')
    
    # The JWT client expects just the user object directly based on App.js
    # .then((user) => setUser(user))
    return jsonify(user_schema.dump(user)), 200


@auth_bp.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return APIResponse.success(message='Logged out successfully')