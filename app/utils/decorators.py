from functools import wraps
from flask import request, jsonify, session
from app.models import User


def require_auth(fn=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = session.get('user_id')
            
            if not user_id:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Authentication required'
                }), 401
            
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Invalid session'
                }), 401
            
            request.current_user = user
            
            return fn(*args, **kwargs)
        return wrapper
    
    if fn is None:
        return decorator
    return decorator(fn)