from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint, UniqueConstraint
from app import db, login_manager

# User Loader for Flask-Login


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Association Table for Favorites (Many-to-Many Relationship)
favorites = db.Table('favorites',
                     db.Column('user_id', db.Integer, db.ForeignKey(
                         'user.id'), primary_key=True),
                     db.Column('movie_id', db.String, db.ForeignKey(
                         'movie.id'), nullable=True),
                     db.Column('tvshow_id', db.String, db.ForeignKey(
                         'tv_show.id'), nullable=True)
                     )


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_picture = db.Column(
        db.String(20), nullable=False, default='default.jpg')
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    favorites = relationship('Favorite', backref='owner', lazy='dynamic')
    reviews = relationship('Review', backref='author', lazy='dynamic')
    recommendations = relationship(
        'Recommendation', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_picture}')"


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.String, primary_key=True)  # Changed to String
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    averageRating = db.Column(db.Float, nullable=True)
    numVotes = db.Column(db.Integer, nullable=True)
    releaseYear = db.Column(db.Integer, nullable=True)
    poster_url = db.Column(db.String(
        500), default='https://via.placeholder.com/300x450.png?text=No+Image')

    trailer_url = db.Column(db.String(1000))
    trailer_fetch_time = db.Column(db.Integer, default=None)

    # Relationships
    reviews = relationship('Review', backref='movie', lazy='dynamic')
    recommendations = relationship(
        'Recommendation', backref='movie', lazy='dynamic')
    favorited_by = relationship('Favorite', backref='movie', lazy='dynamic')

    def __repr__(self):
        return f"Movie('{self.title}', '{self.releaseYear}', '{self.genre}')"


class TVShow(db.Model):
    __tablename__ = 'tv_show'
    id = db.Column(db.String, primary_key=True)  # Changed to String
    title = db.Column(db.String(255), nullable=False)
    seasons = db.Column(db.Integer, nullable=False, default=1)
    episodes = db.Column(db.Integer, nullable=False, default=1)
    release_date = db.Column(db.Date, nullable=False, default=datetime.now)
    genre = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)
    description = db.Column(db.Text, nullable=False,
                            default='No description available.')
    poster_url = db.Column(db.String(
        500), default='https://via.placeholder.com/300x450.png?text=No+Image')

    trailer_url = db.Column(db.String(1000), default=None)
    trailer_fetch_time = db.Column(db.Integer, default=None)

    # Relationships
    reviews = relationship('Review', backref='tv_show', lazy='dynamic')
    recommendations = relationship(
        'Recommendation', backref='tv_show', lazy='dynamic')
    favorited_by = relationship('Favorite', backref='tv_show', lazy='dynamic')

    def __repr__(self):
        return f"TVShow('{self.title}', 'Seasons: {self.seasons}', 'Episodes: {self.episodes}')"


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.String, db.ForeignKey(
        'movie.id'), nullable=True)  # Changed to String
    tvshow_id = db.Column(db.String, db.ForeignKey(
        'tv_show.id'), nullable=True)  # Changed to String

    # Ensure that either movie_id or tvshow_id is provided, not both
    __table_args__ = (
        CheckConstraint(
            '(movie_id IS NOT NULL AND tvshow_id IS NULL) OR (movie_id IS NULL AND tvshow_id IS NOT NULL)',
            name='check_movie_or_tvshow'
        ),
    )

    def __repr__(self):
        if self.movie_id:
            return f"Favorite(User ID: {self.user_id}, Movie ID: {self.movie_id})"
        else:
            return f"Favorite(User ID: {self.user_id}, TVShow ID: {self.tvshow_id})"


class Recommendation(db.Model):
    __tablename__ = 'recommendation'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # 'movie' or 'tv_show'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.String, db.ForeignKey(
        'movie.id'), nullable=True)  # Changed to String
    tvshow_id = db.Column(db.String, db.ForeignKey(
        'tv_show.id'), nullable=True)  # Changed to String

    # Ensure that type matches the presence of movie_id or tvshow_id
    __table_args__ = (
        CheckConstraint(
            "((type = 'movie' AND movie_id IS NOT NULL AND tvshow_id IS NULL) OR "
            "(type = 'tv_show' AND tvshow_id IS NOT NULL AND movie_id IS NULL))",
            name='check_recommendation_type'
        ),
    )

    def __repr__(self):
        if self.type == 'movie' and self.movie_id:
            return f"Recommendation(User ID: {self.user_id}, Movie ID: {self.movie_id})"
        elif self.type == 'tv_show' and self.tvshow_id:
            return f"Recommendation(User ID: {self.user_id}, TVShow ID: {self.tvshow_id})"
        else:
            return f"Recommendation(User ID: {self.user_id})"


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.String, db.ForeignKey(
        'movie.id'), nullable=True)  # Changed to String
    tvshow_id = db.Column(db.String, db.ForeignKey(
        'tv_show.id'), nullable=True)  # Changed to String
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # Ensure that either movie_id or tvshow_id is provided, not both
    # Ensure that rating is between 1 and 10
    __table_args__ = (
        CheckConstraint(
            '(movie_id IS NOT NULL AND tvshow_id IS NULL) OR (movie_id IS NULL AND tvshow_id IS NOT NULL)',
            name='check_review_movie_or_tvshow'
        ),
        CheckConstraint(
            'rating >= 1 AND rating <= 10',
            name='check_review_rating'
        ),
    )

    def __repr__(self):
        if self.movie_id:
            return f"Review(User ID: {self.user_id}, Movie ID: {self.movie_id}, Rating: {self.rating})"
        else:
            return f"Review(User ID: {self.user_id}, TVShow ID: {self.tvshow_id}, Rating: {self.rating})"
