from app.repositories import NoteRepository


class NoteService:
    def __init__(self):
        self.note_repo = NoteRepository()
    
    def get_notes(self, user_id, page=1, per_page=10):
        pagination = self.note_repo.get_by_user_paginated(user_id, page, per_page)
        return {
            'notes': [note.to_dict() for note in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages
        }
    
    def get_note(self, note_id, user_id):
        note = self.note_repo.get_by_id_and_user(note_id, user_id)
        if not note:
            return None, 'Note not found'
        return note, None
    
    def create_note(self, user_id, title, content, category='General', is_pinned=False):
        if not title or not content:
            return None, 'Title and content are required'
        
        note = self.note_repo.create(
            title=title,
            content=content,
            category=category,
            is_pinned=is_pinned,
            user_id=user_id
        )
        return note, None
    
    def update_note(self, note_id, user_id, data):
        note = self.note_repo.get_by_id_and_user(note_id, user_id)
        if not note:
            return None, 'Note not found'
        
        if 'title' in data:
            note.title = data['title']
        if 'content' in data:
            note.content = data['content']
        if 'category' in data:
            note.category = data['category']
        if 'is_pinned' in data:
            note.is_pinned = data['is_pinned']
        
        note = self.note_repo.save(note)
        return note, None
    
    def delete_note(self, note_id, user_id):
        note = self.note_repo.get_by_id_and_user(note_id, user_id)
        if not note:
            return None, 'Note not found'
        
        self.note_repo.delete(note)
        return True, None