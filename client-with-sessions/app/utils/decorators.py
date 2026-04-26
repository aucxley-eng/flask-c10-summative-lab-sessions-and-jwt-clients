from functools import wraps
from flask import request, jsonify, session
from app.models import User


def require_auth(fn=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Try Session Authentication
            user_id = session.get('user_id')
            user = User.query.get(user_id) if user_id else None

            if not user:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Active session required'
                }), 401
            
            request.current_user = user
            
            return fn(*args, **kwargs)
        return wrapper
    
    if fn is None:
        return decorator
    return decorator(fn)