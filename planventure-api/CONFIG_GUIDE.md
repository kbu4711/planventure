# Configuration Guide

## Overview

The PlanVenture API uses a centralized configuration system through `config.py`. Configuration is environment-based with sensible defaults and full support for development, testing, and production environments.

## Configuration File Structure

```
config.py
├── Config (base class)
│   ├── Flask settings
│   ├── Database configuration
│   ├── JWT settings
│   └── CORS configuration
├── DevelopmentConfig
├── TestingConfig
└── ProductionConfig
```

## Environment-Based Configuration

### Development Environment

**Activation:**
```bash
export FLASK_ENV=development
# or in .env
FLASK_ENV=development
```

**Characteristics:**
- Debug mode enabled
- SQLAlchemy Echo enabled (verbose logging)
- Multiple localhost origins allowed
- Less strict CORS validation

**Default CORS Origins:**
```
http://localhost:3000
http://localhost:5173
http://127.0.0.1:3000
http://127.0.0.1:5173
```

### Testing Environment

**Activation:**
```bash
export FLASK_ENV=testing
```

**Characteristics:**
- Debug disabled
- In-memory SQLite database (no persistence)
- Shorter JWT token expiry (300 seconds)
- Testing-friendly CORS settings

**Default Database:** `:memory:` (in-memory)

### Production Environment

**Activation:**
```bash
export FLASK_ENV=production
```

**Characteristics:**
- Debug disabled
- Strict configuration validation
- SQLAlchemy pooling optimized
- Localhost origins rejected

**Required Environment Variables:**
```bash
FLASK_ENV=production
JWT_SECRET_KEY=<your-secret-key>
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

## Configuration Variables

### Flask Configuration

| Variable | Description | Default | Override |
|----------|-------------|---------|----------|
| `DEBUG` | Enable debug mode | Dev: True, Prod: False | `FLASK_DEBUG` |
| `TESTING` | Enable testing mode | False | `FLASK_ENV=testing` |
| `JSON_SORT_KEYS` | Sort JSON keys in responses | False | - |

### Database Configuration

| Variable | Description | Default | Override |
|----------|-------------|---------|----------|
| `SQLALCHEMY_DATABASE_URI` | Database connection string | `sqlite:///planventure.db` | `DATABASE_URL` |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | Track model modifications | False | - |
| `SQLALCHEMY_ECHO` | Log SQL statements | Dev: True, Prod: False | `SQL_ECHO` |
| `SQLALCHEMY_ENGINE_OPTIONS` | Connection pool settings | Pool size: 10 | - |

### JWT Configuration

| Variable | Description | Default | Override |
|----------|-------------|---------|----------|
| `JWT_SECRET_KEY` | Secret key for JWT signing | `dev-secret-key-...` | `JWT_SECRET_KEY` |
| `JWT_ACCESS_TOKEN_EXPIRES` | Access token lifetime | 3600 seconds | `ACCESS_TOKEN_EXPIRES` |
| `JWT_REFRESH_TOKEN_EXPIRES` | Refresh token lifetime | 604800 seconds | `REFRESH_TOKEN_EXPIRES` |
| `JWT_TOKEN_LOCATION` | Token location | `['headers']` | - |
| `JWT_HEADER_NAME` | Authorization header name | `Authorization` | - |
| `JWT_HEADER_TYPE` | Header type prefix | `Bearer` | - |

### CORS Configuration

| Variable | Description | Default | Override |
|----------|-------------|---------|----------|
| `CORS_ORIGINS` | Allowed frontend origins | Dev: `localhost:3000,5173` | `CORS_ORIGINS` |
| `CORS_METHODS` | Allowed HTTP methods | `GET,POST,PUT,DELETE,OPTIONS,PATCH` | - |
| `CORS_ALLOW_HEADERS` | Allowed request headers | `Content-Type,Authorization,X-Requested-With` | - |
| `CORS_EXPOSE_HEADERS` | Exposed response headers | `Content-Type,X-Total-Count,X-Page-Count` | - |
| `CORS_SUPPORTS_CREDENTIALS` | Allow credentials | True | - |
| `CORS_MAX_AGE` | Preflight cache TTL | 3600 seconds | - |
| `CORS_SEND_WILDCARD` | Use wildcard origins | False | - |

## Environment Files

### .env File Example

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

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# SQL Logging (development only)
SQL_ECHO=False
```

### Production .env Example

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False

# Database Configuration
DATABASE_URL=postgresql://user:password@db.example.com:5432/planventure

# JWT Configuration (change these!)
JWT_SECRET_KEY=use-a-strong-random-string-here
ACCESS_TOKEN_EXPIRES=3600
REFRESH_TOKEN_EXPIRES=604800

# CORS Configuration (HTTPS only)
CORS_ORIGINS=https://app.example.com,https://www.example.com
```

## Usage in Application

### Loading Configuration

```python
from config import config

# Automatic loading based on FLASK_ENV
app.config.from_object(config)
```

### Accessing Configuration

```python
from config import config

# In application code
origins = config.get_cors_origins()
secret_key = config.JWT_SECRET_KEY
database_uri = config.SQLALCHEMY_DATABASE_URI
```

### Getting CORS Origins

The `get_cors_origins()` method safely parses and cleans up CORS origins:

```python
# From config
origins = config.get_cors_origins()
# Returns: ['http://localhost:3000', 'http://localhost:5173']

# With custom origins
os.environ['CORS_ORIGINS'] = 'https://app.com,https://www.app.com'
origins = config.get_cors_origins()
# Returns: ['https://app.com', 'https://www.app.com']
```

## Configuration Priority

Settings are applied in this order (highest to lowest priority):

1. **Environment Variables** (`FLASK_ENV=...`)
2. **`.env` File** (loaded by python-dotenv)
3. **Environment-Specific Config Class** (DevelopmentConfig, etc.)
4. **Base Config Class** (defaults)

Example:
```bash
# This becomes the active configuration
export FLASK_ENV=production

# Which loads settings from ProductionConfig class
# Which can be overridden by environment variables
export JWT_SECRET_KEY=custom-value
```

## Production Deployment Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Change `JWT_SECRET_KEY` to a strong random value
- [ ] Set `DATABASE_URL` to production database
- [ ] Configure `CORS_ORIGINS` with your domain
- [ ] Use HTTPS URLs in CORS_ORIGINS
- [ ] Verify JWT token expiry times
- [ ] Test database connectivity
- [ ] Enable SQLALCHEMY_ENGINE_OPTIONS pooling
- [ ] Set up proper logging
- [ ] Run security validation

## Security Best Practices

1. **Never commit .env files**
   ```gitignore
   .env
   .env.local
   .env.*.local
   ```

2. **Use strong JWT secrets**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **HTTPS only in production**
   - Use `https://` URLs only
   - Never use `http://` in production CORS_ORIGINS

4. **Environment variables for secrets**
   - Store secrets in environment, not code
   - Never log secrets
   - Rotate periodically

5. **Database security**
   - Use connection pooling (default enabled)
   - Set minimum required permissions
   - Use SSL for remote databases

6. **CORS specificity**
   - List only required origins
   - No wildcard (`*`) in production
   - Credentials only with specific origins

## Troubleshooting

### "JWT_SECRET_KEY must be set in production"

**Cause:** Using default secret in production

**Solution:**
```bash
export JWT_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')
```

### "CORS_ORIGINS must be set in production"

**Cause:** No CORS origins configured for production

**Solution:**
```env
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

### "Production CORS_ORIGINS cannot contain localhost"

**Cause:** Localhost origins in production configuration

**Solution:** Update CORS_ORIGINS to use actual domain names

### Configuration Not Loading

**Check environment:**
```python
from config import config
print(f"Environment: {os.getenv('FLASK_ENV')}")
print(f"Config class: {config.__class__.__name__}")
```

## References

- [Flask Configuration Handbook](https://flask.palletsprojects.com/config/)
- [Environment Variables on Heroku](https://devcenter.heroku.com/articles/config-vars)
- [12 Factor App - Config](https://12factor.net/config)
