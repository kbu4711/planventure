# Trip Management Routes Documentation

## Overview

The Trip routes provide complete CRUD (Create, Read, Update, Delete) operations for managing travel trips in the PlanVenture API. All endpoints require authentication via JWT token.

## Base URL
```
/api/trips
```

## Authentication

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Endpoints

### 1. Create Trip
**Endpoint:** `POST /api/trips`

Create a new trip for the authenticated user.

**Request:**
```json
{
  "destination": "Paris, France",
  "start_date": "2026-06-01T00:00:00",
  "end_date": "2026-06-15T00:00:00",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "description": "Summer vacation in Paris"
}
```

**Response (201 Created):**
```json
{
  "message": "Trip created successfully",
  "data": {
    "id": 1,
    "user_id": 1,
    "destination": "Paris, France",
    "start_date": "2026-06-01T00:00:00",
    "end_date": "2026-06-15T00:00:00",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "description": "Summer vacation in Paris",
    "itinerary_items": [],
    "created_at": "2026-03-30T15:55:44.613840",
    "updated_at": "2026-03-30T15:55:44.613840"
  }
}
```

**Status Codes:**
- `201` - Trip created successfully
- `400` - Invalid input or validation error
- `401` - Unauthorized (missing/invalid token)
- `500` - Server error

**Validation Rules:**
- `destination` (required): String, 1-255 characters
- `start_date` (required): ISO datetime, must be before end_date
- `end_date` (required): ISO datetime, must be after start_date
- `latitude` (optional): Float, valid latitude value
- `longitude` (optional): Float, valid longitude value
- `description` (optional): String

---

### 2. Get All Trips
**Endpoint:** `GET /api/trips`

Retrieve all trips for the authenticated user with pagination.

**Query Parameters:**
- `limit` - Maximum trips to return (default: 50, max: 1000)
- `offset` - Number of trips to skip for pagination (default: 0)

**Example:**
```
GET /api/trips?limit=10&offset=20
```

**Response (200 OK):**
```json
{
  "message": "Trips retrieved successfully",
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "destination": "Paris, France",
      "start_date": "2026-06-01T00:00:00",
      "end_date": "2026-06-15T00:00:00",
      "latitude": 48.8566,
      "longitude": 2.3522,
      "description": "Summer vacation in Paris",
      "itinerary_items": [],
      "created_at": "2026-03-30T15:55:44.613840",
      "updated_at": "2026-03-30T15:55:44.613840"
    }
  ],
  "pagination": {
    "total": 5,
    "limit": 10,
    "offset": 20
  }
}
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized
- `500` - Server error

**Ordering:**
Trips are returned ordered by `start_date` in descending order (upcoming trips first).

---

### 3. Get Single Trip
**Endpoint:** `GET /api/trips/<trip_id>`

Retrieve a specific trip by ID. Only accessible if user owns the trip.

**Example:**
```
GET /api/trips/1
```

**Response (200 OK):**
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
    "itinerary_items": [],
    "created_at": "2026-03-30T15:55:44.613840",
    "updated_at": "2026-03-30T15:55:44.613840"
  }
}
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized
- `403` - Forbidden (user doesn't own trip)
- `404` - Trip not found
- `500` - Server error

---

### 4. Update Trip
**Endpoint:** `PUT /api/trips/<trip_id>`

Update a specific trip (all fields are optional). Only accessible if user owns the trip.

**Request (any combination of fields):**
```json
{
  "destination": "Lyon, France",
  "start_date": "2026-07-01T00:00:00",
  "end_date": "2026-07-10T00:00:00",
  "latitude": 45.7640,
  "longitude": 4.8357,
  "description": "Updated description"
}
```

**Response (200 OK):**
```json
{
  "message": "Trip updated successfully",
  "data": {
    "id": 1,
    "user_id": 1,
    "destination": "Lyon, France",
    "start_date": "2026-07-01T00:00:00",
    "end_date": "2026-07-10T00:00:00",
    "latitude": 45.7640,
    "longitude": 4.8357,
    "description": "Updated description",
    "itinerary_items": [],
    "created_at": "2026-03-30T15:55:44.613840",
    "updated_at": "2026-03-30T15:56:12.123456"
  }
}
```

**Status Codes:**
- `200` - Update successful
- `400` - Invalid input or validation error
- `401` - Unauthorized
- `403` - Forbidden (user doesn't own trip)
- `404` - Trip not found
- `500` - Server error

**Validation Rules:**
- Partial updates allowed (update only fields you need)
- If both dates updated, start_date must still be before end_date
- Same field validation as Create Trip applies to provided fields

---

### 5. Delete Trip
**Endpoint:** `DELETE /api/trips/<trip_id>`

Permanently delete a trip. Only accessible if user owns the trip.

**Example:**
```
DELETE /api/trips/1
```

**Response (200 OK):**
```json
{
  "message": "Trip deleted successfully",
  "data": {
    "id": 1,
    "destination": "Paris, France"
  }
}
```

**Status Codes:**
- `200` - Delete successful
- `401` - Unauthorized
- `403` - Forbidden (user doesn't own trip)
- `404` - Trip not found
- `500` - Server error

**Note:** Deleting a trip also deletes all associated itinerary items (cascade delete).

---

### 6. Get Trip Statistics
**Endpoint:** `GET /api/trips/<trip_id>/stats`

Get statistics about a specific trip (e.g., duration, number of activities).

**Example:**
```
GET /api/trips/1/stats
```

**Response (200 OK):**
```json
{
  "message": "Trip statistics retrieved successfully",
  "data": {
    "trip_id": 1,
    "destination": "Paris, France",
    "total_days": 14,
    "total_activities": 8,
    "start_date": "2026-06-01T00:00:00",
    "end_date": "2026-06-15T00:00:00"
  }
}
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized
- `403` - Forbidden (user doesn't own trip)
- `404` - Trip not found
- `500` - Server error

---

## Common Patterns

### Create a Trip and Get Its Stats

```bash
# 1. Create trip
curl -X POST http://localhost:5000/api/trips \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris, France",
    "start_date": "2026-06-01T00:00:00",
    "end_date": "2026-06-15T00:00:00",
    "latitude": 48.8566,
    "longitude": 2.3522
  }'

# 2. Get statistics (use trip_id from response)
curl -X GET http://localhost:5000/api/trips/1/stats \
  -H "Authorization: Bearer <token>"
```

### List and Update Trips

```bash
# 1. Get all trips with pagination
curl -X GET "http://localhost:5000/api/trips?limit=5&offset=0" \
  -H "Authorization: Bearer <token>"

# 2. Update a trip
curl -X PUT http://localhost:5000/api/trips/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated vacation plans"
  }'
```

### Partial Update Example

```bash
# Update only the destination and description
curl -X PUT http://localhost:5000/api/trips/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "London, UK",
    "description": "Changed destination to London"
  }'
```

---

## Error Responses

### Validation Error (400)
```json
{
  "error": "validation_error",
  "message": "Invalid input data",
  "errors": {
    "start_date": ["Start date must be before end date"]
  }
}
```

### Unauthorized (401)
```json
{
  "error": "token_expired",
  "message": "Your session has expired. Please login again."
}
```

### Forbidden (403)
```json
{
  "error": "forbidden",
  "message": "You do not have permission to access this trip"
}
```

### Not Found (404)
```json
{
  "error": "not_found",
  "message": "Trip not found"
}
```

### Server Error (500)
```json
{
  "error": "server_error",
  "message": "An error occurred while creating the trip"
}
```

---

## Testing with Bruno/Postman

### Setup
1. Register a user (POST /api/auth/register)
2. Copy the `access_token` from response
3. In Bruno: Auth → Bearer Token → Paste token

### Test Workflow
```
1. POST /api/trips - Create a trip
2. GET /api/trips - List all trips
3. GET /api/trips/1 - Get single trip
4. PUT /api/trips/1 - Update trip
5. GET /api/trips/1/stats - Get statistics
6. DELETE /api/trips/1 - Delete trip
```

---

## Data Models

### Trip Object
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Trip ID (auto-generated) |
| user_id | Integer | Owner's user ID |
| destination | String | Trip destination |
| start_date | DateTime | Trip start date/time |
| end_date | DateTime | Trip end date/time |
| latitude | Float | Destination latitude |
| longitude | Float | Destination longitude |
| description | String | Trip description/notes |
| itinerary_items | Array | List of activities/events |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

---

## Best Practices

1. **Always verify user owns trip before operations**
   - API automatically validates ownership for all operations

2. **Use pagination for lists**
   - Default limit is 50, max is 1000
   - Use offset for pagination: `?limit=10&offset=20`

3. **Validate dates on client side**
   - start_date must be before end_date
   - Use ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`

4. **Handle errors gracefully**
   - Check status code and error field
   - Display user-friendly error messages from `message` field

5. **Access trip data efficiently**
   - Use GET /api/trips/<id>/stats for quick stats
   - Use GET /api/trips/<id> for full trip details with itinerary

---

## Limitations & Considerations

- **Cascade Delete:** Deleting a trip also deletes all itinerary items
- **User Isolation:** Each user can only see/modify their own trips
- **Date Validation:** Start date must be strictly before end date
- **Pagination:** Maximum 1000 trips per request (configurable)
- **Coordinates Optional:** Latitude/longitude not required but recommended

---

## Future Enhancements

- [ ] Trip sharing with other users
- [ ] Trip templates/duplication
- [ ] Trip archiving (soft delete)
- [ ] Trip categories/tags
- [ ] AI-powered trip suggestions
- [ ] Weather integration for dates
- [ ] Collaborative editing
