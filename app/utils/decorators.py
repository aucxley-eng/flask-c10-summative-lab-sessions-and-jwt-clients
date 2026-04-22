from functools import wraps
from flask import request, jsonify, session
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User


def require_auth(fn=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = None
            
            # 1. Try Session Authentication
            user_id = session.get('user_id')
            if user_id:
                user = User.query.get(user_id)
            
            # 2. Try JWT Authentication if Session fails
            if not user:
                try:
                    # verify_jwt_in_request() will raise an exception if JWT is invalid or missing
                    verify_jwt_in_request(optional=True)
                    jwt_user_id = get_jwt_identity()
                    if jwt_user_id:
                        user = User.query.get(jwt_user_id)
                except Exception:
                    pass

            if not user:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Authentication required'
                }), 401
            
            request.current_user = user
            
            return fn(*args, **kwargs)
        return wrapper
    
    if fn is None:
        return decorator
    return decorator(fn)