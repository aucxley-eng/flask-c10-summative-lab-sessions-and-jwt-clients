from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User, Note

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    password_confirmation = data.get('password_confirmation')
    
    if not username or not password:
        return jsonify({'errors': ['Username and password are required']}), 400
    
    if password != password_confirmation:
        return jsonify({'errors': ['Password confirmation does not match']}), 400
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'errors': ['Username already exists']}), 400
    
    user = User(username=username)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    session['user_id'] = user.id
    
    return jsonify(user.to_dict()), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'errors': ['Username and password are required']}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({'errors': ['Invalid username or password']}), 401
    
    session['user_id'] = user.id
    
    return jsonify(user.to_dict()), 200


@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({}), 200
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({}), 200
    
    return jsonify(user.to_dict()), 200


@auth_bp.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return jsonify({}), 200