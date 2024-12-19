from app import create_app, db
from app.models import User, Movie, TVShow, Favorite, Recommendation, Review
from sqlalchemy import text

def clear_data():
    db.session.execute(text('TRUNCATE TABLE "user" CASCADE'))
    db.session.execute(text('TRUNCATE TABLE movie CASCADE'))
    db.session.execute(text('TRUNCATE TABLE tv_show CASCADE'))
    db.session.execute(text('TRUNCATE TABLE favorite CASCADE'))
    db.session.execute(text('TRUNCATE TABLE recommendation CASCADE'))
    db.session.execute(text('TRUNCATE TABLE review CASCADE'))
    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        clear_data()
        print("All data cleared from the database.")