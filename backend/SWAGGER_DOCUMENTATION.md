# Swagger/OpenAPI Documentation Guide

## Overview

The Eventsarthi API now includes comprehensive Swagger/OpenAPI documentation that allows you to:
- View all available API endpoints
- Understand request/response schemas
- Test API endpoints directly from the browser
- Generate client SDKs automatically

## Accessing Swagger UI

Once the application is running, you can access the interactive API documentation at:

### Swagger UI (Interactive)
```
http://localhost:8000/docs
```

### ReDoc (Alternative Documentation)
```
http://localhost:8000/redoc
```

### OpenAPI JSON Schema
```
http://localhost:8000/openapi.json
```

## Features Implemented

### 1. Enhanced Main Application Configuration
- **Comprehensive API Description**: Detailed overview of the platform
- **Contact Information**: Support details for API users
- **License Information**: MIT License details
- **Tags Metadata**: Organized endpoints by category
- **Custom Swagger UI Parameters**: Enhanced UI with syntax highlighting and filtering

### 2. Pydantic Schemas Created

#### Authentication Schemas (`app/schemas/auth.py`)
- `PlannerRegister`: Registration request
- `PlannerLogin`: Login credentials
- `Token`: Authentication token response
- `TokenRefresh`: Token refresh request
- `PasswordReset`: Password reset request
- `PasswordResetConfirm`: Password reset confirmation
- `EmailVerification`: Email verification
- `PlannerResponse`: Planner profile response
- `MessageResponse`: Generic message response

#### Event Schemas (`app/schemas/event.py`)
- `EventCreate`: Create new event
- `EventUpdate`: Update event details
- `EventResponse`: Event details response
- `EventListResponse`: Paginated event list
- `EventStats`: Event statistics
- `EventType`: Event type enumeration
- `EventStatus`: Event status enumeration

#### Guest Schemas (`app/schemas/guest.py`)
- `GuestCreate`: Add new guest
- `GuestUpdate`: Update guest details
- `GuestResponse`: Guest details response
- `GuestListResponse`: Paginated guest list
- `GuestStats`: Guest/RSVP statistics
- `BulkGuestImport`: Bulk import guests
- `RSVPStatus`: RSVP status enumeration

### 3. Enhanced API Routes

All API routes now include:
- **Detailed Descriptions**: Clear explanation of what each endpoint does
- **Request/Response Models**: Typed schemas for validation
- **Response Status Codes**: All possible HTTP responses documented
- **Example Data**: Sample requests and responses
- **Query Parameters**: Documented with descriptions and constraints
- **Authentication Requirements**: Clearly marked protected endpoints

## API Endpoint Categories

### 🔐 Authentication (`/api/v1/auth`)
- `POST /register` - Register new planner
- `POST /login` - Login and get tokens
- `POST /refresh` - Refresh access token
- `POST /logout` - Logout current session
- `POST /verify-email` - Verify email address
- `POST /forgot-password` - Request password reset
- `POST /reset-password` - Reset password with token
- `GET /me` - Get current planner profile

### 📅 Events (`/api/v1/events`)
- `POST /` - Create new event
- `GET /` - List all events (paginated)
- `GET /stats` - Get event statistics
- `GET /{event_id}` - Get event details
- `PUT /{event_id}` - Update event
- `DELETE /{event_id}` - Delete event
- `POST /{event_id}/complete` - Mark event as completed

### 👥 Guests (`/api/v1/guests`)
- `POST /{event_id}/guests` - Add guest to event
- `GET /{event_id}/guests` - List event guests (paginated)
- `GET /{event_id}/guests/stats` - Get RSVP statistics
- `GET /{event_id}/guests/{guest_id}` - Get guest details
- `PUT /{event_id}/guests/{guest_id}` - Update guest
- `DELETE /{event_id}/guests/{guest_id}` - Delete guest
- `POST /{event_id}/guests/import` - Bulk import guests

### 💬 Conversations (`/api/v1/conversations`)
- WhatsApp conversation management endpoints

### 📢 Broadcasts (`/api/v1/broadcasts`)
- Mass messaging and campaign management endpoints

### 🎯 Support Requests (`/api/v1/support-requests`)
- Guest support ticket management endpoints

### 📊 Analytics (`/api/v1/analytics`)
- Event analytics and reporting endpoints

### 🔗 Webhooks (`/api/v1/webhooks`)
- WhatsApp webhook endpoints for receiving messages

## Using Swagger UI

### 1. Testing Endpoints

1. Navigate to `http://localhost:8000/docs`
2. Find the endpoint you want to test
3. Click on the endpoint to expand it
4. Click "Try it out" button
5. Fill in the required parameters
6. Click "Execute"
7. View the response below

### 2. Authentication

For protected endpoints:

1. Click the "Authorize" button at the top right
2. Enter your JWT token in the format: `Bearer <your_token>`
3. Click "Authorize"
4. Now you can test protected endpoints

### 3. Exploring Schemas

- Click on "Schemas" at the bottom of the page
- View all request/response models
- See field types, constraints, and examples

## Running the Application

### Prerequisites
```bash
cd backend
pip install -r requirements.txt
```

### Start the Server
```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the main.py directly
python -m app.main
```

### Access Documentation
Once running, open your browser to:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

The Swagger UI configuration is in `backend/app/main.py`:

```python
app = FastAPI(
    title="Eventsarthi API",
    description=description,
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": 1,
        "defaultModelExpandDepth": 1,
        "docExpansion": "list",
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "syntaxHighlight.theme": "monokai",
    }
)
```

## Generating Client SDKs

You can generate client SDKs in various languages using the OpenAPI schema:

### Using OpenAPI Generator
```bash
# Install OpenAPI Generator
npm install @openapitools/openapi-generator-cli -g

# Generate Python client
openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g python \
  -o ./client-python

# Generate TypeScript/JavaScript client
openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g typescript-axios \
  -o ./client-typescript
```

## Best Practices

1. **Always document new endpoints** with:
   - Clear summary and description
   - Request/response models
   - All possible status codes
   - Example data

2. **Use Pydantic schemas** for:
   - Request validation
   - Response serialization
   - Automatic documentation

3. **Include examples** in schemas:
   - Use `json_schema_extra` in Config class
   - Provide realistic sample data

4. **Tag endpoints appropriately**:
   - Use consistent tag names
   - Group related endpoints together

5. **Document authentication**:
   - Mark protected endpoints with `Depends(get_current_planner)`
   - Document required permissions

## Troubleshooting

### Swagger UI not loading
- Check if the server is running
- Verify the port (default: 8000)
- Check browser console for errors

### Endpoints not showing
- Ensure routers are included in main.py
- Check for syntax errors in route definitions
- Verify imports are correct

### Schema validation errors
- Check Pydantic model definitions
- Ensure field types match
- Verify required vs optional fields

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)

## Support

For issues or questions:
- Email: support@eventsarthi.com
- Documentation: https://eventsarthi.com/docs
- GitHub Issues: [Create an issue]

---

**Made with Bob** 🤖