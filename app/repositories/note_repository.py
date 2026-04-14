from app.models import Note
from app.repositories.base_repository import BaseRepository


class NoteRepository(BaseRepository):
    def __init__(self):
        super().__init__(Note)
    
    def get_by_user(self, user_id):
        return Note.query.filter_by(user_id=user_id).all()
    
    def get_by_user_paginated(self, user_id, page=1, per_page=10):
        return Note.query.filter_by(user_id=user_id).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    def get_by_id_and_user(self, note_id, user_id):
        return Note.query.filter_by(id=note_id, user_id=user_id).first()