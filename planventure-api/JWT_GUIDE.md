# JWT Authentication Utilities

Complete JWT token generation and validation functions for secure API authentication.

## Setup

JWT is automatically initialized in `app.py`. Just ensure `jwt_utils.py` is imported:

```python
from jwt_utils import setup_jwt
jwt = setup_jwt(app)
```

## Configuration

Set the following environment variables in your `.env` file:

```env
JWT_SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRES=3600        # 1 hour in seconds
REFRESH_TOKEN_EXPIRES=604800     # 7 days in seconds
```

## Core Functions

### 1. Token Generation

#### `generate_tokens(user_id, email=None) -> Dict`
Generate both access and refresh tokens for a user.

```python
from jwt_utils import generate_tokens

tokens = generate_tokens(user_id=1, email="user@example.com")
# Returns: {
#     'access_token': '...',
#     'refresh_token': '...',
#     'token_type': 'Bearer',
#     'expires_in': 3600
# }
```

### 2. Token Validation

#### `decode_token(token, verify=True) -> Dict | None`
Decode a JWT token and return its payload.

```python
from jwt_utils import decode_token

payload = decode_token(access_token)
if payload:
    user_id = payload['sub']
    email = payload.get('email')
```

#### `validate_token_payload(token) -> Tuple[bool, Dict, str]`
Comprehensive token validation with error information.

```python
from jwt_utils import validate_token_payload

is_valid, payload, error = validate_token_payload(token)
if not is_valid:
    print(f"Token invalid: {error}")
```

### 3. Getting Current User

#### `get_current_user_id() -> int | None`
Get the authenticated user's ID (use within @jwt_required() endpoint).

```python
from flask_jwt_extended import jwt_required
from jwt_utils import get_current_user_id

@app.route('/profile')
@jwt_required()
def get_profile():
    user_id = get_current_user_id()
    return jsonify({'user_id': user_id})
```

#### `get_token_claims() -> Dict | None`
Get additional claims from JWT token.

```python
from jwt_utils import get_token_claims

@app.route('/profile')
@jwt_required()
def get_profile():
    claims = get_token_claims()
    email = claims.get('email')
```

### 4. Utility Functions

#### `extract_token_from_request() -> str | None`
Extract JWT token from Authorization header.

```python
from jwt_utils import extract_token_from_request

token = extract_token_from_request()
```

#### `create_token_response(user_id, email=None, message='Login successful') -> Dict`
Create a complete token response for API endpoints.

```python
from jwt_utils import create_token_response

response = create_token_response(1, "user@example.com")
return jsonify(response), 200
```

#### `refresh_token_endpoint_response(refresh_token) -> Tuple[Dict, int]`
Generate response for token refresh endpoint.

```python
from flask_jwt_extended import jwt_required
from jwt_utils import refresh_token_endpoint_response

@app.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    refresh_token = request.form.get('refresh_token')
    response, status = refresh_token_endpoint_response(refresh_token)
    return jsonify(response), status
```

## Decorators

### `@token_required`
Alternative to `@jwt_required()` for simpler syntax.

```python
from jwt_utils import token_required, get_current_user_id

@app.route('/protected')
@token_required
def protected_route():
    user_id = get_current_user_id()
    return jsonify({'user_id': user_id})
```

### `@optional_token`
Make JWT optional - user info available if provided, but endpoint accessible without it.

```python
from jwt_utils import optional_token, get_current_user_id

@app.route('/posts')
@optional_token
def list_posts():
    user_id = get_current_user_id()
    if user_id:
        # Return user's posts
    else:
        # Return public posts
```

## Example Authorization Header

When making API requests, include the access token in the Authorization header:

```bash
curl -H "Authorization: Bearer <access_token>" http://api.example.com/protected
```

Or in Python:

```python
import requests

headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get('http://api.example.com/protected', headers=headers)
```

## Token Structure

### Access Token
- **Expires**: 1 hour (configurable)
- **Used for**: API endpoint authentication
- **Type**: Bearer token

### Refresh Token
- **Expires**: 7 days (configurable)
- **Used for**: Obtaining new access tokens
- **Type**: Bearer token

## Error Handling

The utilities handle common JWT errors:

- **Expired Token**: `token has expired`
- **Invalid Token**: `Invalid token: ...`
- **Missing Token**: `Token is missing`
- **Malformed Token**: `Invalid token: ...`

## Security Best Practices

1. **Change JWT_SECRET_KEY in production** - Use a strong, random secret
2. **Use HTTPS** - Always transmit tokens over secure connections
3. **Store tokens securely** - Use httpOnly cookies or secure storage on client
4. **Short expiration times** - Access tokens should expire quickly
5. **Refresh tokens offline** - Validate refresh tokens carefully

## Testing

```python
from app import app
from jwt_utils import generate_tokens, decode_token

with app.app_context():
    # Generate tokens
    tokens = generate_tokens(1, "test@example.com")
    
    # Verify token
    payload = decode_token(tokens['access_token'])
    assert payload['sub'] == 1
    assert payload['email'] == "test@example.com"
```

## Integration with Flask-JWT-Extended

This module wraps `flask-jwt-extended` with additional utilities:

- Built-in error handling
- Simplified token generation
- Type hints for better IDE support
- Configuration management
- Response formatting

For advanced features, see [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
