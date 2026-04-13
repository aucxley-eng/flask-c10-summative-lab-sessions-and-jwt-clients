from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User, Note

notes_bp = Blueprint('notes', __name__)


def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)


@notes_bp.route('', methods=['GET'])
def get_notes():
    user = get_current_user()
    if not user:
        return jsonify({'errors': ['Authentication required']}), 401
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    notes = Note.query.filter_by(user_id=user.id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'notes': [note.to_dict() for note in notes.items],
        'total': notes.total,
        'page': notes.page,
        'per_page': notes.per_page,
        'pages': notes.pages
    }), 200


@notes_bp.route('', methods=['POST'])
def create_note():
    user = get_current_user()
    if not user:
        return jsonify({'errors': ['Authentication required']}), 401
    
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    
    if not title or not content:
        return jsonify({'errors': ['Title and content are required']}), 400
    
    note = Note(title=title, content=content, user_id=user.id)
    db.session.add(note)
    db.session.commit()
    
    return jsonify(note.to_dict()), 201


@notes_bp.route('/<int:note_id>', methods=['GET'])
def get_note(note_id):
    user = get_current_user()
    if not user:
        return jsonify({'errors': ['Authentication required']}), 401
    
    note = Note.query.filter_by(id=note_id, user_id=user.id).first()
    
    if not note:
        return jsonify({'errors': ['Note not found']}), 404
    
    return jsonify(note.to_dict()), 200


@notes_bp.route('/<int:note_id>', methods=['PATCH'])
def update_note(note_id):
    user = get_current_user()
    if not user:
        return jsonify({'errors': ['Authentication required']}), 401
    
    note = Note.query.filter_by(id=note_id, user_id=user.id).first()
    
    if not note:
        return jsonify({'errors': ['Note not found']}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    
    db.session.commit()
    
    return jsonify(note.to_dict()), 200


@notes_bp.route('/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    user = get_current_user()
    if not user:
        return jsonify({'errors': ['Authentication required']}), 401
    
    note = Note.query.filter_by(id=note_id, user_id=user.id).first()
    
    if not note:
        return jsonify({'errors': ['Note not found']}), 404
    
    db.session.delete(note)
    db.session.commit()
    
    return jsonify({}), 200