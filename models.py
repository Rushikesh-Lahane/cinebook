from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """Registered users of the system."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"


class Genre(db.Model):
    """Movie genres / categories."""
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    movies = db.relationship('Movie', backref='genre', lazy=True)

    def __repr__(self):
        return f"<Genre {self.name}>"


class Movie(db.Model):
    """Movie catalogue with full metadata."""
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    director = db.Column(db.String(100), nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)  # e.g. 148
    language = db.Column(db.String(50), default='English')
    rating = db.Column(db.String(10), nullable=True)         # e.g. 'U/A', 'A', 'U'
    release_date = db.Column(db.Date, nullable=True)
    poster_url = db.Column(db.String(300), nullable=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    shows = db.relationship('Show', backref='movie', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Movie {self.title}>"


class Screen(db.Model):
    """Physical screens / halls inside the theatre."""
    __tablename__ = 'screens'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)          # e.g. 'Screen 1', 'IMAX Hall'
    total_seats = db.Column(db.Integer, nullable=False)

    shows = db.relationship('Show', backref='screen', lazy=True)

    def __repr__(self):
        return f"<Screen {self.name}>"


class Show(db.Model):
    """A specific screening of a movie in a screen at a date/time."""
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    screen_id = db.Column(db.Integer, db.ForeignKey('screens.id'), nullable=False)
    show_date = db.Column(db.Date, nullable=False)
    show_time = db.Column(db.String(20), nullable=False)     # e.g. '10:30 AM'
    ticket_price = db.Column(db.Float, nullable=False, default=200.0)
    available_seats = db.Column(db.Integer, nullable=False)

    # Relationships
    bookings = db.relationship('Booking', backref='show', lazy=True)

    def __repr__(self):
        return f"<Show {self.movie_id} @ {self.show_date} {self.show_time}>"


class Booking(db.Model):
    """A seat booking made by a user for a specific show."""
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    booking_ref = db.Column(db.String(20), unique=True, nullable=False)  # e.g. 'BK202400001'
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(150), nullable=True)
    seats_booked = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmed')   # confirmed / cancelled
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Booking {self.booking_ref} - {self.customer_name}>"
