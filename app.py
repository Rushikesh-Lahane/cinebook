from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Genre, Movie, Screen, Show, Booking
from datetime import date, datetime
import random, string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cinebook-secret-2024'
db.init_app(app)

def generate_booking_ref():
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"BK{datetime.utcnow().strftime('%Y%m%d')}{suffix}"

def seed_data():
    if Movie.query.first():
        return
    genres = {g: Genre(name=g) for g in [
        'Action', 'Sci-Fi', 'Drama', 'Thriller',
        'Comedy', 'Animation', 'Biography', 'Horror', 'Romance'
    ]}
    db.session.add_all(genres.values())
    db.session.flush()

    screens = [
        Screen(name='Screen 1 - Standard', total_seats=120),
        Screen(name='Screen 2 - IMAX',     total_seats=80),
        Screen(name='Screen 3 - 4DX',      total_seats=60),
    ]
    db.session.add_all(screens)
    db.session.flush()

    movies_data = [
        dict(title='Dune: Part Two',
             description='Paul Atreides unites with Chani and the Fremen to wage war against the evil Harkonnen.',
             director='Denis Villeneuve', duration_minutes=166, language='English', rating='U/A',
             release_date=date(2024,3,1), genre_id=genres['Sci-Fi'].id,
             poster_url='/static/posters/dune.jpg',
             trailer_url='https://www.youtube.com/embed/Way9Dexny3w'),
        dict(title='Oppenheimer',
             description='The story of J. Robert Oppenheimer and the invention of the atomic bomb.',
             director='Christopher Nolan', duration_minutes=180, language='English', rating='U/A',
             release_date=date(2023,7,21), genre_id=genres['Biography'].id,
             poster_url='/static/posters/oppenheimer.jpg',
             trailer_url='https://www.youtube.com/embed/uYPbbksJxIg'),
        dict(title='Inception',
             description='A thief who steals corporate secrets through dream-sharing technology.',
             director='Christopher Nolan', duration_minutes=148, language='English', rating='U/A',
             release_date=date(2010,7,16), genre_id=genres['Sci-Fi'].id,
             poster_url='/static/posters/inception.jpg',
             trailer_url='https://www.youtube.com/embed/YoHD9XEInc0'),
        dict(title='Interstellar',
             description='A team of explorers travel through a wormhole in search of a new home for humanity.',
             director='Christopher Nolan', duration_minutes=169, language='English', rating='U/A',
             release_date=date(2014,11,7), genre_id=genres['Sci-Fi'].id,
             poster_url='/static/posters/interstellar.jpg',
             trailer_url='https://www.youtube.com/embed/zSWdZVtXT7E'),
        dict(title='Inside Out 2',
             description='Riley navigates the complexities of teenage emotions with new feelings joining the mix.',
             director='Kelsey Mann', duration_minutes=100, language='English', rating='U',
             release_date=date(2024,6,14), genre_id=genres['Animation'].id,
             poster_url='/static/posters/insideout2.jpg',
             trailer_url='https://www.youtube.com/embed/LEjhY15eCx0'),
        dict(title='The Dark Knight',
             description='Batman faces the Joker, a criminal mastermind who wants to plunge Gotham into anarchy.',
             director='Christopher Nolan', duration_minutes=152, language='English', rating='U/A',
             release_date=date(2008,7,18), genre_id=genres['Action'].id,
             poster_url='/static/posters/darkknight.jpg',
             trailer_url='https://www.youtube.com/embed/EXeTwQWrcwY'),
        dict(title='Avengers: Endgame',
             description='The Avengers assemble once more to reverse the devastation caused by Thanos.',
             director='Anthony Russo', duration_minutes=181, language='English', rating='U/A',
             release_date=date(2019,4,26), genre_id=genres['Action'].id,
             poster_url='/static/posters/endgame.jpg',
             trailer_url='https://www.youtube.com/embed/TcMBFSGVi1c'),
        dict(title='The Godfather',
             description='The aging patriarch of an organized crime dynasty transfers control to his reluctant son.',
             director='Francis Ford Coppola', duration_minutes=175, language='English', rating='A',
             release_date=date(1972,3,24), genre_id=genres['Drama'].id,
             poster_url='/static/posters/godfather.jpg',
             trailer_url='https://www.youtube.com/embed/sY1S34973zA'),
        dict(title='Joker',
             description='A failed comedian begins a downward spiral into madness in 1980s Gotham City.',
             director='Todd Phillips', duration_minutes=122, language='English', rating='A',
             release_date=date(2019,10,4), genre_id=genres['Thriller'].id,
             poster_url='/static/posters/joker.jpg',
             trailer_url='https://www.youtube.com/embed/zAGVQLHvwOY'),
    ]

    movies = []
    for m in movies_data:
        movie = Movie(**m)
        movies.append(movie)
        db.session.add(movie)
    db.session.flush()

    today = date.today()

    # Full day schedule with 2-hour gap between each show
    # Show times covering entire day from morning to night
    show_schedule = [
        ('09:00 AM', 180.0, 0),   # Morning
        ('11:30 AM', 180.0, 1),   # Late Morning
        ('02:00 PM', 220.0, 2),   # Afternoon
        ('04:30 PM', 220.0, 0),   # Evening
        ('07:00 PM', 250.0, 1),   # Prime Time
        ('09:30 PM', 250.0, 2),   # Night
        ('11:59 PM', 200.0, 0),   # Late Night
    ]

    for i, movie in enumerate(movies):
        for show_time, price, screen_idx in show_schedule:
            scr = screens[(screen_idx + i) % 3]
            db.session.add(Show(
                movie_id=movie.id,
                screen_id=scr.id,
                show_date=today,
                show_time=show_time,
                ticket_price=price,
                available_seats=scr.total_seats,
            ))

    from werkzeug.security import generate_password_hash
    db.session.add(User(
        name='Admin', email='admin@cinebook.com',
        password_hash=generate_password_hash('Admin@123'), is_admin=True
    ))
    db.session.commit()
    print("[INFO] Sample data seeded successfully.")

def generate_todays_shows():
    today = date.today()
    if Show.query.filter_by(show_date=today).first():
        return
    movies = Movie.query.filter_by(is_active=True).all()
    screens = Screen.query.all()
    if not movies or not screens:
        return
    show_schedule = [
        ('09:00 AM', 180.0), ('11:30 AM', 180.0),
        ('02:00 PM', 220.0), ('04:30 PM', 220.0),
        ('07:00 PM', 250.0), ('09:30 PM', 250.0),
        ('11:59 PM', 200.0),
    ]
    for i, movie in enumerate(movies):
        for j, (show_time, price) in enumerate(show_schedule):
            scr = screens[(i + j) % len(screens)]
            db.session.add(Show(
                movie_id=movie.id, screen_id=scr.id,
                show_date=today, show_time=show_time,
                ticket_price=price, available_seats=scr.total_seats,
            ))
    db.session.commit()
    print(f"[INFO] Shows generated for {today}.")


with app.app_context():
    db.create_all()
    seed_data()
    generate_todays_shows()

@app.route('/')
def home():
    movies = Movie.query.filter_by(is_active=True).all()
    genres = Genre.query.all()
    return render_template('index.html', movies=movies, genres=genres)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    shows = Show.query.filter_by(movie_id=movie_id, show_date=date.today()).all()
    return render_template('movie_detail.html', movie=movie, shows=shows)

@app.route('/book/<int:show_id>', methods=['GET', 'POST'])
def book(show_id):
    show = Show.query.get_or_404(show_id)
    if request.method == 'POST':
        name  = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        seats = int(request.form.get('seats', 0))
        if not name or seats <= 0:
            flash("Please enter a valid name and seat count.", "danger")
            return redirect(url_for('book', show_id=show.id))
        if seats > 10:
            flash("Maximum 10 seats per booking.", "warning")
            return redirect(url_for('book', show_id=show.id))
        if show.available_seats < seats:
            flash(f"Only {show.available_seats} seats left!", "danger")
            return redirect(url_for('book', show_id=show.id))
        total = seats * show.ticket_price
        ref   = generate_booking_ref()
        db.session.add(Booking(
            booking_ref=ref, show_id=show.id, user_id=session.get('user_id'),
            customer_name=name, customer_email=email,
            seats_booked=seats, total_amount=total
        ))
        show.available_seats -= seats
        db.session.commit()
        flash(f"Booking confirmed! Reference: {ref}", "success")
        return redirect(url_for('booking_confirmation', ref=ref))
    return render_template('booking.html', show=show)

@app.route('/confirmation/<ref>')
def booking_confirmation(ref):
    booking = Booking.query.filter_by(booking_ref=ref).first_or_404()
    return render_template('confirmation.html', booking=booking)

@app.route('/bookings')
def view_bookings():
    bookings = Booking.query.order_by(Booking.booked_at.desc()).all()
    return render_template('bookings.html', bookings=bookings)

@app.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.status == 'cancelled':
        flash("Booking already cancelled.", "warning")
    else:
        booking.show.available_seats += booking.seats_booked
        booking.status = 'cancelled'
        db.session.commit()
        flash(f"Booking {booking.booking_ref} has been cancelled.", "info")
    return redirect(url_for('view_bookings'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        from werkzeug.security import check_password_hash
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user     = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id']   = user.id
            session['user_name'] = user.name
            session['is_admin']  = user.is_admin
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for('dashboard'))
        flash("Invalid email or password.", "danger")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        from werkzeug.security import generate_password_hash
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip()
        phone    = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "warning")
            return redirect(url_for('register'))
        db.session.add(User(name=name, email=email, phone=phone,
                            password_hash=generate_password_hash(password)))
        db.session.commit()
        flash("Account created! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    user_id  = session.get('user_id')
    bookings = (Booking.query.filter_by(user_id=user_id)
                .order_by(Booking.booked_at.desc()).limit(10).all()) if user_id else []
    return render_template('dashboard.html', bookings=bookings)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
