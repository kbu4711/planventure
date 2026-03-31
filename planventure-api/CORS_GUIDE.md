# CORS Configuration Guide

## Overview

This API is configured with CORS (Cross-Origin Resource Sharing) to support requests from React frontend applications. CORS is essential for browser-based applications to make requests to an API hosted on a different domain or port.

## Current Configuration

### Default Allowed Origins
- `http://localhost:3000` - Create React App development server
- `http://localhost:5173` - Vite development server

### Allowed Methods
- GET
- POST
- PUT
- DELETE
- OPTIONS
- PATCH

### Allowed Headers
- `Content-Type` - Standard HTTP content type header
- `Authorization` - Required for JWT token authentication
- `X-Requested-With` - XMLHttpRequest identifier

### Exposed Headers
- `Content-Type` - Response content type
- `X-Total-Count` - For pagination (total count)
- `X-Page-Count` - For pagination (page count)

### Additional Settings
- **Credentials**: Enabled (`supports_credentials=True`)
  - Allows credentials (cookies, authorization headers) to be sent with requests
  - Required for JWT authentication
- **Max Age**: 3600 seconds (1 hour)
  - Preflight responses are cached for 1 hour to reduce unnecessary OPTIONS requests
- **Send Wildcard**: Disabled (`send_wildcard=False`)
  - Uses specific origins instead of wildcard `*` for security

## Environment Configuration

### Development Setup

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Configure CORS origins in `.env`:**
   ```env
   CORS_ORIGINS=http://localhost:3000,http://localhost:5173
   ```

3. **For Create React App:**
   ```env
   CORS_ORIGINS=http://localhost:3000
   ```

4. **For Vite:**
   ```env
   CORS_ORIGINS=http://localhost:5173
   ```

### Production Setup

For production, update CORS origins to your actual frontend domain:

```env
CORS_ORIGINS=https://your-app-name.com,https://www.your-app-name.com
```

### Multiple Origins

To allow multiple frontend URLs:

```env
CORS_ORIGINS=https://app.example.com,https://staging.example.com,https://www.example.com
```

## Frontend Usage

### React with Fetch API

```javascript
// Include credentials in requests for JWT authentication
fetch('http://localhost:5000/api/trips', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`  // JWT token will be sent
  },
  credentials: 'include',  // Include cookies and auth headers
  body: JSON.stringify(tripData)
})
```

### React with Axios

```javascript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api',
  credentials: 'include',  // Enable credentials
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add authorization header before each request
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Make request
apiClient.post('/trips', tripData);
```

## Preflight Requests

Certain requests trigger automatic CORS preflight checks (OPTIONS requests):

**Requests that trigger preflight:**
- Requests with custom headers (like `Authorization`)
- PUT and DELETE requests
- Requests with `Content-Type: application/json`

**Preflight response caching:**
- Preflight responses are cached for 3600 seconds (1 hour)
- This reduces the number of OPTIONS requests to the API

## Troubleshooting

### "Access to XMLHttpRequest blocked by CORS policy"

1. **Check the origin:**
   - Verify your frontend URL matches an allowed origin in `CORS_ORIGINS`
   - Account for port numbers (e.g., `localhost:3000` ≠ `localhost:5000`)

2. **Check the frontend URL:**
   ```javascript
   // Verify this matches an allowed origin
   console.log(window.location.origin);
   ```

3. **Verify credentials are set:**
   ```javascript
   fetch(url, {
     credentials: 'include'  // Required for JWT auth
   })
   ```

### Preflight request fails (OPTIONS 404)

- Ensure `OPTIONS` method is in `ALLOWED_METHODS`
- Verify the API server is running

### Authorization header not sent

1. Ensure `Authorization` is in `ALLOWED_HEADERS`
2. Include `credentials: 'include'` in fetch options or axios config
3. Verify JWT token is in Authorization header: `Authorization: Bearer {token}`

## Security Considerations

⚠️ **Important for Production:**

1. **Never use wildcard origins (`*`) in production**
   - Current configuration uses specific origins only
   - Prevents unauthorized applications from accessing your API

2. **Use HTTPS in production**
   - Always use `https://` URLs in production
   ```env
   # Development
   CORS_ORIGINS=http://localhost:3000
   
   # Production
   CORS_ORIGINS=https://myapp.com,https://www.myapp.com
   ```

3. **Credentials over CORS**
   - `supports_credentials=True` combined with specific origins is secure
   - Client must explicitly set `credentials: 'include'` to send cookies/auth

4. **Limit exposed headers**
   - Only expose headers that clients need access to

## Testing CORS

### Using curl

```bash
# Test with preflight request
curl -i -X OPTIONS http://localhost:5000/api/trips \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type,Authorization"
```

### Using browser console

```javascript
// Test from your React app's browser console
fetch('http://localhost:5000/api/me', {
  headers: {
    'Authorization': `Bearer ${token}`
  },
  credentials: 'include'
})
.then(r => r.json())
.then(data => console.log(data))
.catch(err => console.error('CORS Error:', err))
```

## Reference

- [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)
