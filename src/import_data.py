import csv
import os
import sys
from datetime import datetime
from sqlalchemy import text
from app import create_app, db
from app.models import Movie, TVShow
from utils import fetch_poster  # Ensure utils.py has the fetch_poster function

app = create_app()


def clear_data():
    with app.app_context():
        try:
            truncate_statement = """
            TRUNCATE TABLE review, recommendation, favorite, movie, tv_show, "user" RESTART IDENTITY CASCADE;
            """
            db.session.execute(text(truncate_statement))
            db.session.commit()
            print("All data cleared from the database.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while clearing data: {e}")


def import_data(csv_filepath):
    with app.app_context():
        with open(csv_filepath, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            total_rows = 0
            imported_movies = 0
            imported_tvshows = 0
            skipped_rows = 0

            for row in reader:
                total_rows += 1
                entry_id = row.get('id', '').strip()
                title = row.get('title', '').strip()
                # 'movie', 'tvshow', 'tvseries', 'tvminiseries'
                type_ = row.get('type', '').strip().lower()
                genres = row.get('genres', '').strip()
                averageRating = float(row.get('averageRating', 0)) if row.get(
                    'averageRating') else None
                try:
                    numVotes = int(float(row.get('numVotes', 0))
                                   ) if row.get('numVotes') else None
                except ValueError:
                    numVotes = None
                try:
                    releaseYear = int(float(row.get('releaseYear', 0))) if row.get(
                        'releaseYear') else None
                except ValueError:
                    releaseYear = None

                if not entry_id or not title or not type_ or not genres or averageRating is None or numVotes is None or releaseYear is None:
                    print(
                        f"Row {total_rows}: Missing required fields. Skipping.")
                    skipped_rows += 1
                    continue

                if type_ == 'movie':
                    # Check if the movie already exists to avoid duplicates
                    existing_movie = Movie.query.filter_by(id=entry_id).first()
                    if existing_movie:
                        print(
                            f"Row {total_rows}: Movie with ID '{entry_id}' already exists. Skipping.")
                        skipped_rows += 1
                        continue

                    # poster_url = fetch_poster(title, 'movie')  # Fetch poster URL

                    movie = Movie(
                        id=entry_id,
                        title=title,
                        genre=genres,
                        averageRating=averageRating,
                        numVotes=numVotes,
                        releaseYear=releaseYear,
                        poster_url='https://via.placeholder.com/300x450.png?text=No+Image'
                    )
                    db.session.add(movie)
                    imported_movies += 1

                elif type_ in ['tvseries']:
                    # Check if the TV show already exists to avoid duplicates
                    existing_tvshow = TVShow.query.filter_by(
                        id=entry_id).first()
                    if existing_tvshow:
                        print(
                            f"Row {total_rows}: TV show with ID '{entry_id}' already exists. Skipping.")
                        skipped_rows += 1
                        continue

                    # poster_url = fetch_poster(title, 'series')  # Fetch poster URL

                    tvshow = TVShow(
                        id=entry_id,
                        title=title,
                        genre=genres,
                        seasons=int(row.get('seasons', 0)) if row.get(
                            'seasons') else 1,
                        episodes=int(row.get('episodes', 0)) if row.get(
                            'episodes') else 1,
                        release_date=row.get(
                            'release_date', '').strip() or datetime.now(),
                        description=row.get('description', '').strip(
                        ) or 'No description available.',
                        rating=averageRating if averageRating else 5,
                        poster_url='https://via.placeholder.com/300x450.png?text=No+Image'
                    )
                    db.session.add(tvshow)
                    imported_tvshows += 1

                else:
                    print(
                        f"Row {total_rows}: Unknown type '{type_}'. Skipping.")
                    skipped_rows += 1
                    continue

            # Commit all changes to the database
            db.session.commit()
            print(
                f"Import Completed: {imported_movies} movies and {imported_tvshows} TV shows imported.")
            print(
                f"Total Rows Processed: {total_rows}, Skipped: {skipped_rows}")


if __name__ == '__main__':
    # Define the path to your CSV file
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'top_media.csv')

    if os.path.exists(csv_path):
        clear_data()  # Clear existing data before importing new data
        import_data(csv_path)
    else:
        print(f"CSV file not found at path: {csv_path}")
