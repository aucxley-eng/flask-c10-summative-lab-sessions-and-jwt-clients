from faker import Faker
from app import create_app
from app.models import db, User, Note, generate_api_key

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
            user.api_key = generate_api_key()
            db.session.add(user)
        
        db.session.commit()
        users = User.query.all()
        
        for user in users:
            for _ in range(5):
                note = Note(
                    title=fake.sentence(nb_words=5),
                    content=fake.paragraph(nb_sentences=5),
                    user_id=user.id
                )
                db.session.add(note)
        
        db.session.commit()
        
        print('Database seeded successfully!')
        print(f'Created {len(users)} users with API keys')
        print(f'Created {Note.query.count()} notes')


if __name__ == '__main__':
    seed()