# CineBook – Online Movie Ticket Booking System

A Flask-based web application for booking movie tickets, developed as a BCA Final Year Project.

---

## Features

- Browse currently showing movies with genre filters
- View show timings, screen details, and seat availability in real time
- Book tickets with instant booking reference generation
- Cancel bookings with automatic seat restoration
- User registration and login with hashed passwords
- Admin panel to view all bookings
- User dashboard showing personal booking history

---

## Technology Stack

| Layer      | Technology                      |
|------------|---------------------------------|
| Backend    | Python 3.10+, Flask 3.x         |
| ORM        | Flask-SQLAlchemy 3.x            |
| Database   | SQLite (development)            |
| Security   | Werkzeug password hashing       |
| Frontend   | HTML5, CSS3, Bootstrap 5        |

---

## Database Schema (ERD Summary)

```
users        ←── bookings ──→ shows ──→ movies ──→ genres
                              shows ──→ screens
```

**Tables:** `users`, `genres`, `movies`, `screens`, `shows`, `bookings`

---

## Project Structure

```
moviebook/
├── app.py              # Application entry point & all routes
├── models.py           # SQLAlchemy models (6 tables)
├── requirements.txt    # Python dependencies
├── database.db         # SQLite database (auto-created)
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── movie_detail.html
│   ├── booking.html
│   ├── confirmation.html
│   ├── bookings.html
│   ├── dashboard.html
│   ├── login.html
│   └── register.html
└── static/
    ├── css/style.css
    └── js/main.js
```

---

## Setup & Run

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate          # Linux / macOS
.venv\Scripts\activate             # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python3 app.py
```

The app starts at **http://127.0.0.1:8000/**

The database is created automatically on first run with sample movies, screens, and shows seeded.

---

## Default Admin Credentials

| Field    | Value               |
|----------|---------------------|
| Email    | admin@cinebook.com  |
| Password | Admin@123           |

> ⚠️ Change these credentials before deploying to production.

---

## API / Routes Reference

| Method | URL                      | Description                    |
|--------|--------------------------|--------------------------------|
| GET    | `/`                      | Home – list of movies          |
| GET    | `/movie/<id>`            | Movie detail + show timings    |
| GET/POST | `/book/<show_id>`      | Seat booking form              |
| GET    | `/confirmation/<ref>`    | Booking confirmation / e-ticket|
| GET    | `/bookings`              | Admin – all bookings           |
| POST   | `/cancel/<booking_id>`   | Cancel a booking               |
| GET/POST | `/login`               | User login                     |
| GET/POST | `/register`            | User registration              |
| GET    | `/logout`                | Logout                         |
| GET    | `/dashboard`             | User booking history           |

---

## Future Enhancements

- Online payment gateway integration (Razorpay / Stripe)
- Seat map selection (row/column)
- Email / SMS confirmation via Twilio or SendGrid
- Admin movie & show management CRUD
- Role-based access control (admin vs. user)
- PostgreSQL migration for production

---

## License

This project is developed for academic purposes as a BCA Final Year submission.
