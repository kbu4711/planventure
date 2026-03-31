# PlanVenture API 🚀

[![Flask](https://img.shields.io/badge/Flask-2.3.3-black?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

A comprehensive Flask-based REST API backend for PlanVenture - a trip planning and itinerary management application. Plan your travels with detailed itineraries, meal schedules, accommodations, and activities all in one place.

**[Live API Documentation](http://localhost:5000)** | **[CORS Configuration](planventure-api/CORS_GUIDE.md)** | **[Configuration Guide](planventure-api/CONFIG_GUIDE.md)**

---

## 🎯 Features

✨ **User Management**
- User registration and authentication with JWT tokens
- Secure password hashing with bcrypt
- User profile management

✈️ **Trip Planning**
- Create and manage multiple trips
- Duplicate trip detection (same user, destination, dates)
- Trip CRUD operations with full validation

📅 **Itinerary Management**
- Create detailed itineraries for each day of travel
- Add multiple activities per day with timing
- Schedule meals (breakfast, lunch, dinner)
- Store accommodation details

🔐 **Security**
- JWT-based authentication
- CORS support for React frontend
- Protected and public route management
- Environment-based configuration

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
  - [Local Setup](#local-setup)
  - [Development Server](#development-server)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Endpoints](#endpoints)
- [Configuration](#configuration)
- [Database Schema](#database-schema)
- [Error Handling](#error-handling)
- [Development](#development)
- [Production Deployment](#production-deployment)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)

---

## 📦 Prerequisites

Before you begin, ensure you have the following:

- **Python**: 3.9 or higher ([Download](https://www.python.org/downloads/))
- **Git**: For version control ([Download](https://git-scm.com/downloads))
- **GitHub Account**: For repository access ([Sign up](https://github.com))
- **API Client** (optional): [Bruno](https://github.com/usebruno/bruno) or [Postman](https://www.postman.com/)
- **Code Editor**: [VS Code](https://code.visualstudio.com/) is recommended
- **GitHub Copilot** (optional): For AI-assisted development

---

## 🚀 Quick Start

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd planventure/planventure-api
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate on macOS/Linux
   source venv/bin/activate
   
   # Activate on Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your settings
   ```

5. **Initialize database**
   ```bash
   python init_db.py
   ```

### Development Server

Start the Flask development server:

```bash
flask run
```

Server runs at: `http://localhost:5000`

To use a custom port:
```bash
flask run --port 8000
```

---

## 📚 API Documentation

### Base URL

```
Development:  http://localhost:5000/api
Production:   https://api.planventure.com/api
```

### Authentication

The API uses **JWT (JSON Web Tokens)** for authentication.

**Getting a Token:**
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "data": {
    "access_token": "eyJhbGc...",
    "user_id": 1,
    "email": "user@example.com"
  }
}
```

**Using the Token:**
```bash
Authorization: Bearer eyJhbGc...
```

Include the token in the `Authorization` header for all protected endpoints.

### Endpoints

#### Authentication Routes

**POST `/api/auth/register`** - Register a new user
```bash
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**POST `/api/auth/login`** - Login user
```bash
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**GET `/api/me`** - Get current user info *(Protected)*
```bash
Authorization: Bearer {token}
```

---

#### Trip Routes

**POST `/api/trips`** - Create a new trip *(Protected)*
```bash
Authorization: Bearer {token}
Content-Type: application/json

{
  "destination": "Paris, France",
  "start_date": "2026-06-01T00:00:00",
  "end_date": "2026-06-15T00:00:00",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "description": "Summer vacation in Paris",
  "itinerary_items": [
    {
      "day": 1,
      "title": "Arrival Day",
      "activity_date": "2026-06-01T09:00:00",
      "location": "Paris",
      "breakfast_time": "08:00:00",
      "lunch_time": "12:00:00",
      "dinner_time": "19:00:00",
      "activities": [
        {
          "name": "Airport Transfer",
          "time": "14:00",
          "duration_minutes": 60,
          "location": "CDG Airport"
        }
      ]
    }
  ]
}
```

**GET `/api/trips`** - Get all user trips *(Protected)*
```bash
Authorization: Bearer {token}
Query Parameters:
  - limit: Maximum results (default: 50, max: 1000)
  - offset: Skip results (default: 0)
```

**GET `/api/trips/<trip_id>`** - Get specific trip *(Protected)*
```bash
Authorization: Bearer {token}
```

**Response:**
```json
{
  "message": "Trip retrieved successfully",
  "data": {
    "id": 1,
    "user_id": 1,
    "destination": "Paris, France",
    "start_date": "2026-06-01T00:00:00",
    "end_date": "2026-06-15T00:00:00",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "description": "Summer vacation in Paris",
    "itinerary_items": [
      {
        "id": 1,
        "day": 1,
        "title": "Day 1 - Paris, France",
        "description": "Explore and discover Paris, France",
        "activity_date": "2026-06-01T09:00:00",
        "breakfast_time": "08:00:00",
        "lunch_time": "12:00:00",
        "dinner_time": "19:00:00",
        "accommodation_name": null,
        "accommodation_address": null,
        "activities": [
          {
            "name": "Morning Activity",
            "time": "09:00",
            "duration_minutes": 120,
            "location": "Paris, France",
            "notes": "Add your morning activity here"
          }
        ]
      }
    ],
    "created_at": "2026-03-31T10:00:00",
    "updated_at": "2026-03-31T10:00:00"
  }
}
```

---

#### Itinerary Routes

**GET `/api/trips/<trip_id>/itinerary/items`** - Get itinerary items *(Protected)*
```bash
Authorization: Bearer {token}
Query Parameters:
  - day: Filter by day number (optional)
```

**GET `/api/trips/<trip_id>/itinerary/items/<item_id>`** - Get specific item *(Protected)*
```bash
Authorization: Bearer {token}
```

**POST `/api/trips/<trip_id>/itinerary/items`** - Create itinerary item *(Protected)*
```bash
Authorization: Bearer {token}
Content-Type: application/json

{
  "day": 2,
  "title": "Day 2 - Sightseeing",
  "description": "Visit major attractions",
  "activity_date": "2026-06-02T09:00:00",
  "location": "Paris, France",
  "breakfast_time": "08:00:00",
  "lunch_time": "12:00:00",
  "dinner_time": "19:00:00",
  "accommodation_name": "Hotel de Paris",
  "accommodation_address": "123 Rue de Paris, 75001 Paris",
  "activities": [
    {
      "name": "Eiffel Tower",
      "time": "10:00",
      "duration_minutes": 180,
      "location": "Champ de Mars",
      "notes": "Book tickets online"
    },
    {
      "name": "Lunch at Cafe",
      "time": "13:00",
      "duration_minutes": 90,
      "location": "Left Bank"
    }
  ]
}
```

**PUT `/api/trips/<trip_id>/itinerary/items/<item_id>`** - Update item *(Protected)*
```bash
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Updated Title",
  "activities": [...],
  ...
}
```

**DELETE `/api/trips/<trip_id>/itinerary/items/<item_id>`** - Delete item *(Protected)*
```bash
Authorization: Bearer {token}
```

---

#### System Routes

**GET `/`** - Welcome message
```bash
# No authentication required
```

**GET `/health`** - Health check
```bash
# No authentication required
Response: { "status": "healthy" }
```

**GET `/api/version`** - API version
```bash
# No authentication required
Response: { "version": "1.0.0" }
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `planventure-api` directory:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///planventure.db

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRES=3600
REFRESH_TOKEN_EXPIRES=604800

# CORS Configuration for React Frontend
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# API Configuration
API_HOST=127.0.0.1
API_PORT=5000
```

**For Production:**
```env
FLASK_ENV=production
FLASK_DEBUG=False
JWT_SECRET_KEY=<use-strong-random-key>
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/planventure
```

See [CONFIG_GUIDE.md](planventure-api/CONFIG_GUIDE.md) for detailed configuration options.

---

## 📊 Database Schema

### Users Table
```sql
users
├── id (Primary Key)
├── email (Unique)
├── password (Hashed)
├── created_at (Timestamp)
└── updated_at (Timestamp)
```

### Trips Table
```sql
trips
├── id (Primary Key)
├── user_id (Foreign Key → users)
├── destination (String)
├── start_date (DateTime)
├── end_date (DateTime)
├── latitude (Float, nullable)
├── longitude (Float, nullable)
├── description (Text, nullable)
├── created_at (Timestamp)
└── updated_at (Timestamp)
```

### Itinerary Items Table
```sql
itinerary_items
├── id (Primary Key)
├── trip_id (Foreign Key → trips)
├── day (Integer)
├── title (String)
├── description (Text, nullable)
├── activity_date (DateTime)
├── latitude (Float, nullable)
├── longitude (Float, nullable)
├── location (String, nullable)
├── breakfast_time (Time, nullable)
├── lunch_time (Time, nullable)
├── dinner_time (Time, nullable)
├── accommodation_name (String, nullable)
├── accommodation_address (Text, nullable)
├── activities (JSON)
├── created_at (Timestamp)
└── updated_at (Timestamp)
```

---

## ❌ Error Handling

The API returns standardized error responses:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "errors": {}
}
```

### Common HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | GET request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate trip |
| 500 | Server Error | Unexpected error |

**Example Error Response:**
```json
{
  "error": "validation_error",
  "message": "Invalid input data",
  "errors": {
    "destination": ["Shorter than minimum length 1"],
    "start_date": ["Missing data for required field"]
  }
}
```

---

## 🔧 Development

### Project Structure

```
planventure-api/
├── app.py                 # Flask application factory
├── config.py              # Configuration management
├── database.py            # SQLAlchemy setup
├── init_db.py             # Database initialization
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── models/
│   ├── __init__.py
│   ├── user.py           # User model
│   ├── trip.py           # Trip model
│   └── itinerary_item.py # Itinerary item model
├── routes/
│   ├── __init__.py
│   ├── auth.py           # Authentication endpoints
│   ├── trips.py          # Trip endpoints
│   └── itinerary.py      # Itinerary endpoints
├── schemas/
│   └── *.py              # Marshmallow validation schemas
├── docs/
│   ├── CORS_GUIDE.md     # CORS configuration
│   ├── CONFIG_GUIDE.md   # Configuration guide
│   └── AUTH_API.md       # Authentication API docs
└── instance/
    └── planventure.db    # SQLite database (dev only)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=

# Run specific test
pytest tests/test_auth.py
```

### Code Formatting

```bash
# Format with Black
black planventure-api/

# Lint with Flake8
flake8 planventure-api/
```

---

## 🚀 Production Deployment

### Prerequisites

1. Production database (PostgreSQL recommended)
2. HTTPS certificate
3. Environment secrets configured
4. Frontend domain configured for CORS

### Deployment Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Configure strong `JWT_SECRET_KEY`
- [ ] Set up PostgreSQL or production database
- [ ] Configure `CORS_ORIGINS` with your domain
- [ ] Enable HTTPS only
- [ ] Set up proper logging
- [ ] Configure error monitoring (e.g., Sentry)
- [ ] Run security audit
- [ ] Test database backups

### Deployment Platforms

**Heroku:**
```bash
heroku login
git push heroku main
heroku config:set FLASK_ENV=production
```

**AWS:**
- Use Elastic Beanstalk or App Runner
- RDS for PostgreSQL database
- CloudFront for CDN

**Docker:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app"]
```

---

## 📝 API Usage Examples

### Complete Workflow

**1. Register User**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "traveler@example.com",
    "password": "secure123"
  }'
```

**2. Create Trip with Itinerary**
```bash
curl -X POST http://localhost:5000/api/trips \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo, Japan",
    "start_date": "2026-07-01T00:00:00",
    "end_date": "2026-07-10T00:00:00",
    "latitude": 35.6762,
    "longitude": 139.6503,
    "description": "Exploring Tokyo"
  }'
```

**3. Get All Trips**
```bash
curl -X GET http://localhost:5000/api/trips \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**4. Update Itinerary Item**
```bash
curl -X PUT http://localhost:5000/api/trips/1/itinerary/items/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Day 1",
    "activities": [...]
  }'
```

---

## 🐛 Troubleshooting

### Common Issues

**"CORS error" on frontend requests**
- Check `CORS_ORIGINS` environment variable
- Verify frontend URL is in allowed origins
- Ensure credentials are set in fetch/axios

**"JWT token invalid" error**
- Verify token is in `Authorization: Bearer` format
- Check token hasn't expired
- Confirm `JWT_SECRET_KEY` matches on server

**"Database locked" error**
- Too many concurrent connections
- Check SQLite pooling settings
- Consider upgrading to PostgreSQL

**Port already in use**
```bash
# Find process using port
lsof -i :5000
# Kill process
kill -9 <PID>
```

### Debug Mode

Enable detailed logging:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
flask run
```

---

## 📖 Additional Documentation

- [CORS Configuration Guide](planventure-api/CORS_GUIDE.md)
- [Configuration Management](planventure-api/CONFIG_GUIDE.md)
- [Authentication API](planventure-api/AUTH_API.md)
- [Trip Routes](planventure-api/TRIP_ROUTES.md)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 💬 Support

For issues and questions:

- Open an issue on GitHub
- Check existing documentation
- Contact the development team

---

## 🎉 Acknowledgments

- Flask framework
- Flask-CORS for CORS handling
- Flask-JWT-Extended for authentication
- Marshmallow for data validation
- Python-dotenv for environment management

---

**Made with ❤️ by the PlanVenture Team**