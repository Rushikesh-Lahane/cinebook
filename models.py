from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='user', lazy=True)


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    movies = db.relationship('Movie', backref='genre', lazy=True)


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    director = db.Column(db.String(100), nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)
    language = db.Column(db.String(50), default='English')
    rating = db.Column(db.String(10), nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    poster_url = db.Column(db.String(300), nullable=True)
    trailer_url = db.Column(db.String(300), nullable=True)   # YouTube embed URL
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    shows = db.relationship('Show', backref='movie', lazy=True, cascade='all, delete-orphan')


class Screen(db.Model):
    __tablename__ = 'screens'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    shows = db.relationship('Show', backref='screen', lazy=True)


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    screen_id = db.Column(db.Integer, db.ForeignKey('screens.id'), nullable=False)
    show_date = db.Column(db.Date, nullable=False)
    show_time = db.Column(db.String(20), nullable=False)
    ticket_price = db.Column(db.Float, nullable=False, default=200.0)
    available_seats = db.Column(db.Integer, nullable=False)
    bookings = db.relationship('Booking', backref='show', lazy=True)


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    booking_ref = db.Column(db.String(20), unique=True, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(150), nullable=True)
    seats_booked = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmed')
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)
