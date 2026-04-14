from functools import wraps
from flask import request, jsonify
from app.models import User


def require_auth(fn=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            
            if not api_key:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'API key required. Include X-API-Key header.'
                }), 401
            
            user = User.query.filter_by(api_key=api_key).first()
            
            if not user:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Invalid API key.'
                }), 401
            
            request.current_user = user
            
            return fn(*args, **kwargs)
        return wrapper
    
    if fn is None:
        return decorator
    return decorator(fn)