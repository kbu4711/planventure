# Authentication API Routes

Complete authentication system with user registration, login, email validation, and password strength checking.

## Base URL

```
/api/auth
```

## Endpoints

### 1. Register User

Register a new user account with email and password.

**Endpoint:** `POST /api/auth/register`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "created_at": "2026-03-30T14:55:23.600361"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

**Error Responses:**

- **400 Bad Request** - Invalid input or weak password:
```json
{
  "error": "weak_password",
  "message": "Password does not meet strength requirements",
  "requirements": [
    "Password must be at least 8 characters long",
    "Password must contain at least one uppercase letter",
    "Password must contain at least one special character (!@#$%^&*)"
  ],
  "score": 2
}
```

- **409 Conflict** - Email already registered:
```json
{
  "error": "email_exists",
  "message": "This email is already registered. Please use a different email or login."
}
```

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)
- At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

---

### 2. Login User

Authenticate user with email and password.

**Endpoint:** `POST /api/auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "created_at": "2026-03-30T14:55:23.600361"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": "invalid_credentials",
  "message": "Invalid email or password"
}
```

---

### 3. Validate Email

Check if an email address is valid and available for registration.

**Endpoint:** `POST /api/auth/validate-email`

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "email": "user@example.com",
  "is_valid": true,
  "is_available": true,
  "message": "Email is available"
}
```

**Invalid Email Response:**
```json
{
  "email": "invalid-email",
  "is_valid": false,
  "is_available": false,
  "message": "Invalid email format"
}
```

**Email Exists Response:**
```json
{
  "email": "taken@example.com",
  "is_valid": true,
  "is_available": false,
  "message": "Email is already registered"
}
```

---

### 4. Check Password Strength

Validate password strength without registering.

**Endpoint:** `POST /api/auth/check-password-strength`

**Request:**
```json
{
  "password": "MySecure123!"
}
```

**Response (200 OK):**
```json
{
  "is_strong": true,
  "score": 5,
  "requirements": {
    "length": true,
    "has_uppercase": true,
    "has_lowercase": true,
    "has_digit": true,
    "has_special": true
  },
  "message": "Password is strong"
}
```

**Weak Password Response:**
```json
{
  "is_strong": false,
  "score": 2,
  "requirements": {
    "length": true,
    "has_uppercase": false,
    "has_lowercase": true,
    "has_digit": false,
    "has_special": false
  },
  "message": "Password does not meet all strength requirements"
}
```

**Strength Scoring:**
- 0-2: Very Weak
- 3: Weak
- 4: Good
- 5: Strong

---

### 5. Logout

Logout the current user session.

**Endpoint:** `POST /api/auth/logout`

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

## Using Tokens

### Authorization Header

Include the access token in request headers to access protected endpoints:

```bash
curl -H "Authorization: Bearer <access_token>" \
  http://api.example.com/api/protected
```

### Python Example

```python
import requests

headers = {
    'Authorization': f'Bearer {access_token}'
}
response = requests.get('http://api.example.com/api/protected', headers=headers)
```

### JavaScript Example

```javascript
const headers = {
  'Authorization': `Bearer ${accessToken}`
};

fetch('http://api.example.com/api/protected', {
  method: 'GET',
  headers: headers
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Token Details

### Access Token
- **Type:** Bearer Token (JWT)
- **Expiration:** 1 hour (configurable)
- **Usage:** Access protected API endpoints
- **Format:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ...`

### Refresh Token
- **Type:** Bearer Token (JWT)
- **Expiration:** 7 days (configurable)
- **Usage:** Obtain new access tokens when expired
- **Format:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ...`

---

## Email Validation

Email validation includes:
- Format validation (RFC 5322)
- Length check (max 255 characters)
- Database uniqueness check

### Valid Email Examples
- user@example.com
- john.doe@company.co.uk
- sales+tag@business.org

### Invalid Email Examples
- user@
- @example.com
- user name@example.com
- user@example

---

## Error Codes

| Error | HTTP Status | Description |
|-------|------------|-------------|
| `validation_error` | 400 | Invalid input data |
| `weak_password` | 400 | Password doesn't meet strength requirements |
| `email_invalid` | 400 | Email format is invalid |
| `email_exists` | 409 | Email already registered |
| `invalid_credentials` | 401 | Wrong email or password |
| `server_error` | 500 | Internal server error |

---

## Security Considerations

1. **Password Storage:** Passwords are hashed using PBKDF2-SHA256 with salt
2. **Token Security:** Use HTTPS in production
3. **Token Expiration:** Access tokens expire after 1 hour
4. **Token Storage:** Store tokens securely (httpOnly cookies recommended)
5. **Rate Limiting:** Implement rate limiting on auth endpoints (recommended)
6. **Input Validation:** All inputs are validated server-side

---

## Flow Examples

### Registration Flow

```
1. User submits email and password
2. Server validates email format
3. Server checks if email is available
4. Server validates password strength
5. Server hashes password
6. Server creates user in database
7. Server generates access and refresh tokens
8. Server returns tokens to client
```

### Login Flow

```
1. User submits email and password
2. Server validates input format
3. Server finds user by email
4. Server verifies password against hash
5. Server generates access and refresh tokens
6. Server returns tokens to client
```

### Email Validation Flow

```
1. Client submits candidate email
2. Server validates email format
3. Server checks database for existing email
4. Server returns validation result
```

---

## Testing

### cURL Examples

**Register:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123!"}'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123!"}'
```

**Validate Email:**
```bash
curl -X POST http://localhost:5000/api/auth/validate-email \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```

**Check Password Strength:**
```bash
curl -X POST http://localhost:5000/api/auth/check-password-strength \
  -H "Content-Type: application/json" \
  -d '{"password":"TestPass123!"}'
```

---

## Related Documentation

- [JWT Authentication Guide](JWT_GUIDE.md)
- [Password Security](password_utils.py)
- [User Model](models/user.py)
