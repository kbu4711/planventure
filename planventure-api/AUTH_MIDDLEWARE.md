# Authentication Middleware Documentation

## Overview

The `auth_middleware.py` module provides decorators and utilities to protect Flask routes with JWT authentication. It makes it easy to require authentication on specific routes while allowing flexible access control.

## Quick Start

### Basic Protected Route

```python
from auth_middleware import protected_route
from flask import jsonify
from auth_middleware import get_current_user_id

@app.route('/api/protected')
@protected_route
def protected_endpoint():
    user_id = get_current_user_id()
    return jsonify({'message': f'Hello user {user_id}'}), 200
```

**Requirements:**
- Client must send Authorization header with valid JWT token
- Returns 401 if token is missing, invalid, or expired

---

## Decorators

### 1. `@protected_route`

Requires a valid JWT token. Route returns 401 Unauthorized if token is missing or invalid.

```python
@app.route('/api/trips')
@protected_route
def get_user_trips():
    user_id = get_current_user_id()
    # Fetch trips for user_id
    return jsonify({'trips': [...]}), 200
```

**Returns:**
- `200` - Success with route logic
- `401` - No token, invalid token, or expired token
- `403` - (Forbidden - reserved for role checks)

**Status codes in response:**
- `token_expired` - Token has expired, re-login required
- `invalid_token` - Malformed or corrupted token
- `auth_error` - Generic authentication failure

---

### 2. `@optional_auth`

Route works with or without authentication. If a token is provided and valid, user info is available in `g.user_id`.

```python
@app.route('/api/public-trips')
@optional_auth
def get_public_trips():
    user_id = get_current_user_id()
    
    if user_id:
        # Return personalized trip list
        return jsonify({'trips': [...], 'personalized': True}), 200
    else:
        # Return generic trip list (anonymous)
        return jsonify({'trips': [...], 'anonymous': True}), 200
```

**Behavior:**
- If valid token provided: `g.user_id` is set to user ID
- If invalid/expired token: `g.user_id` is `None`, route still executes
- If no token: `g.user_id` is `None`, route still executes

---

### 3. `@require_roles(*roles)` (Requires `@protected_route`)

Requires user to have specific role(s). Must be used with `@protected_route`.

```python
@app.route('/api/admin/users')
@protected_route
@require_roles('admin')
def admin_users():
    return jsonify({'users': [...]}), 200

@app.route('/api/settings')
@protected_route
@require_roles('admin', 'moderator')  # Accepts multiple roles
def admin_settings():
    return jsonify({'settings': {...}}), 200
```

**Note:** Requires that JWT tokens include `roles` claim. Currently not implemented in `jwt_utils.py` but framework is ready.

**Returns:**
- `403` - User doesn't have required role

---

## Utility Functions

### `get_current_user_id()`
Get the current authenticated user's ID.

```python
from auth_middleware import get_current_user_id

user_id = get_current_user_id()
if user_id:
    print(f"Authenticated as: {user_id}")
else:
    print("Not authenticated")
```

**Returns:** User ID (int) or None

---

### `is_authenticated()`
Check if the current request is authenticated.

```python
from auth_middleware import is_authenticated

if is_authenticated():
    # Do something for authenticated users
    pass
else:
    # Do something for anonymous users
    pass
```

**Returns:** Boolean

---

### `get_auth_header()`
Extract the Bearer token from Authorization header.

```python
from auth_middleware import get_auth_header

token = get_auth_header()
if token:
    print(f"Token: {token}")
else:
    print("No token in header")
```

**Returns:** Token string or None

---

## Using with Flask-RESTful

If using Flask-RESTful, you can still apply decorators to methods:

```python
from flask_restful import Api, Resource
from auth_middleware import protected_route

class UserTripsResource(Resource):
    @protected_route
    def get(self):
        user_id = get_current_user_id()
        return {'trips': [...]}, 200
    
    @protected_route
    def post(self):
        user_id = get_current_user_id()
        return {'created': True}, 201

api = Api(app)
api.add_resource(UserTripsResource, '/api/trips')
```

---

## Custom Error Handling

The middleware automatically handles common JWT errors:

| Error | Status | Message |
|-------|--------|---------|
| Token expired | 401 | `token_expired` - Your session has expired. Please login again. |
| Invalid token | 401 | `invalid_token` - Invalid or malformed token. |
| No token | 401 | (Flask-JWT-Extended default) |
| Missing role | 403 | `insufficient_permissions` - This endpoint requires one of: {roles} |

---

## Accessing JWT Claims

Store JWT claims in `g` object for use in route handlers:

```python
from flask import g
from auth_middleware import protected_route

@app.route('/api/claims')
@protected_route
def get_claims():
    user_id = g.user_id  # User ID from 'sub' claim
    claims = g.jwt_claims  # Full JWT claims dict
    
    return jsonify({
        'user_id': user_id,
        'email': claims.get('email'),
        'iat': claims.get('iat'),
        'exp': claims.get('exp')
    }), 200
```

---

## Testing Protected Routes

### Using cURL

```bash
# First, get a token by registering/logging in
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'

# Response includes access_token
# Response:
# {
#   "data": {
#     "access_token": "eyJ...",
#     "refresh_token": "eyJ...",
#     ...
#   }
# }

# Now use token to access protected route
curl -X GET http://localhost:5000/api/me \
  -H "Authorization: Bearer eyJ..."
```

### Using Bruno/Postman

1. Register a user (POST /api/auth/register)
2. Copy `access_token` from response
3. In Bruno: Go to "Auth" tab → Set to "Bearer Token"
4. Paste the token
5. Send request to protected endpoint

---

## Common Patterns

### Pattern 1: User-Specific Data

```python
@app.route('/api/trips/<int:trip_id>')
@protected_route
def get_trip(trip_id):
    user_id = get_current_user_id()
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({'error': 'not_found'}), 404
    
    return jsonify({'trip': trip.to_dict()}), 200
```

The `user_id` ensures users can only access their own trips.

---

### Pattern 2: Conditional Response Based on Auth

```python
@app.route('/api/trips')
@optional_auth
def list_trips():
    user_id = get_current_user_id()
    
    if user_id:
        # Return user's private trips
        trips = Trip.query.filter_by(user_id=user_id).all()
    else:
        # Return public trips only
        trips = Trip.query.filter_by(is_public=True).all()
    
    return jsonify({'trips': [t.to_dict() for t in trips]}), 200
```

---

### Pattern 3: Admin-Only Routes

```python
@app.route('/api/admin/users')
@protected_route
@require_roles('admin')
def list_all_users():
    users = User.query.all()
    return jsonify({'users': [u.to_dict() for u in users]}), 200
```

*Note: Requires role support in JWT generation*

---

## Example Routes Added to app.py

Three example routes have been added to `app.py`:

1. **GET /api/me** - Protected route returning current user info
2. **GET /api/protected-test** - Simple protected route
3. **GET /api/optional-test** - Optional auth example

Test them:
```bash
# Protected route (requires token)
curl -H "Authorization: Bearer <token>" http://localhost:5000/api/me

# Optional auth (works with or without token)
curl http://localhost:5000/api/optional-test
```

---

## Migration Guide: Protecting Existing Routes

To add authentication to an existing route:

**Before:**
```python
@app.route('/api/trips')
def get_trips():
    return jsonify({'trips': [...]}), 200
```

**After:**
```python
from auth_middleware import protected_route, get_current_user_id

@app.route('/api/trips')
@protected_route
def get_trips():
    user_id = get_current_user_id()
    return jsonify({'trips': [...]}), 200
```

That's it! Now the route requires a valid JWT token.

---

## Best Practices

1. **Always use `@protected_route` for sensitive operations**
   - User data modifications
   - Financial transactions
   - Personal information access

2. **Use `@optional_auth` for public endpoints that benefit from personalization**
   - Trip discovery (but show recommendations if authenticated)
   - Search results (personalized if authenticated)

3. **Extract user ID early in route handler**
   ```python
   user_id = get_current_user_id()
   ```

4. **Validate user owns the resource**
   ```python
   # This prevents user1 from accessing user2's data
   trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
   ```

5. **Use meaningful error messages**
   ```python
   return jsonify({
       'error': 'forbidden',
       'message': 'You do not have permission to access this trip'
   }), 403
   ```

---

## Troubleshooting

### "Invalid token" error even with valid token

- Check token format: Must be `Authorization: Bearer <token>`
- Check token expiration: Default is 1 hour
- Check JWT secret key matches between generation and validation

### Route not requiring auth

- Decorator applied? Check `@protected_route` is present
- Duplicate imports causing issues? Use: `from auth_middleware import protected_route`

### Can't access g.user_id in route

- Make sure route has `@protected_route` decorator
- `g.user_id` is set by the middleware
- Access it: `user_id = get_current_user_id()`

---

## Future Enhancements

1. **Role-based access control (RBAC)**
   - Add roles to JWT generation
   - Use `@require_roles()` decorator

2. **Permission scopes**
   - Fine-grained permission control
   - Token scopes for OAuth2 compatibility

3. **Rate limiting**
   - Per-user rate limits
   - Throttle authentication attempts

4. **Audit logging**
   - Log protected route access
   - Track failed auth attempts
