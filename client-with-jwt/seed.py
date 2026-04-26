from faker import Faker
from app import create_app
from app.models import db, User, Note

fake = Faker()


def seed():
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
        db.session.query(Note).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        users = []
        for i in range(3):
            user = User(
                username=fake.user_name() + str(i),
                email=fake.email()
            )
            user.set_password('password123')
            db.session.add(user)
        
        db.session.commit()
        users = User.query.all()
        
        categories = ['Work', 'Personal', 'Shopping', 'Ideas']
        for user in users:
            for _ in range(5):
                note = Note(
                    title=fake.sentence(nb_words=5),
                    content=fake.paragraph(nb_sentences=5),
                    category=fake.random_element(elements=categories),
                    is_pinned=fake.boolean(),
                    user_id=user.id
                )
                db.session.add(note)
        
        db.session.commit()
        
        print('Database seeded successfully!')
        print(f'Created {len(users)} users')
        print(f'Created {Note.query.count()} notes')


if __name__ == '__main__':
    seed()