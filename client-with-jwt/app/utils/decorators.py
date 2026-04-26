from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User


def require_auth(fn=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # verify_jwt_in_request() will raise an exception if JWT is invalid or missing
                verify_jwt_in_request()
                jwt_user_id = get_jwt_identity()
                user = User.query.get(jwt_user_id)
            except Exception:
                user = None

            if not user:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Valid JWT token required'
                }), 401
            
            request.current_user = user
            
            return fn(*args, **kwargs)
        return wrapper
    
    if fn is None:
        return decorator
    return decorator(fn)