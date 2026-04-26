from flask import Blueprint, request
from app.services import NoteService
from app.schemas import NoteSchema
from app.utils.decorators import require_auth
from app.responses import APIResponse

notes_bp = Blueprint('notes', __name__)
note_schema = NoteSchema()


@notes_bp.route('', methods=['GET'])
@require_auth()
def get_notes():
    user = request.current_user
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    note_service = NoteService()
    result = note_service.get_notes(user.id, page, per_page)
    
    return APIResponse.success(data=result)


@notes_bp.route('', methods=['POST'])
@require_auth()
def create_note():
    data = request.get_json() or {}
    user = request.current_user
    
    note_service = NoteService()
    note, error = note_service.create_note(
        user.id, 
        data.get('title'), 
        data.get('content'),
        category=data.get('category', 'General'),
        is_pinned=data.get('is_pinned', False)
    )
    
    if error:
        return APIResponse.error(error, 'Validation Error', 400)
    
    return APIResponse.success(
        data={'note': note_schema.dump(note)},
        message='Note created successfully',
        status_code=201
    )


@notes_bp.route('/<int:note_id>', methods=['GET'])
@require_auth()
def get_note(note_id):
    user = request.current_user
    
    note_service = NoteService()
    note, error = note_service.get_note(note_id, user.id)
    
    if error:
        return APIResponse.not_found(error)
    
    return APIResponse.success(data={'note': note_schema.dump(note)})


@notes_bp.route('/<int:note_id>', methods=['PATCH'])
@require_auth()
def update_note(note_id):
    data = request.get_json() or {}
    user = request.current_user
    
    note_service = NoteService()
    note, error = note_service.update_note(note_id, user.id, data)
    
    if error:
        return APIResponse.not_found(error)
    
    return APIResponse.success(
        data={'note': note_schema.dump(note)},
        message='Note updated successfully'
    )


@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@require_auth()
def delete_note(note_id):
    user = request.current_user
    
    note_service = NoteService()
    _, error = note_service.delete_note(note_id, user.id)
    
    if error:
        return APIResponse.not_found(error)
    
    return APIResponse.success(message='Note deleted successfully')