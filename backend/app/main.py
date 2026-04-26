"""
FastAPI Application Entry Point
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import engine, Base
from app.api.v1 import (
    auth,
    planners,
    events,
    guests,
    conversations,
    broadcasts,
    support_requests,
    analytics,
    webhooks
)
from app.middleware.tenant_isolation import TenantIsolationMiddleware
from app.middleware.rate_limiting import RateLimitMiddleware
from app.middleware.logging import LoggingMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.ENVIRONMENT == "production" else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("Starting Eventsarthi Backend...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    
    # Create database tables (in production, use Alembic migrations)
    if settings.ENVIRONMENT == "development":
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Eventsarthi Backend...")


# Swagger/OpenAPI Configuration
description = """
## Eventsarthi API - AI-Powered Event Management Platform 🎉

This API provides comprehensive event management capabilities with WhatsApp integration and AI-powered assistance.

### Key Features

* **Authentication** - Secure planner registration and login
* **Event Management** - Create, update, and manage events
* **Guest Management** - Handle guest lists and RSVPs
* **WhatsApp Integration** - Automated messaging and conversations
* **AI Assistant** - Intelligent event planning support
* **Analytics** - Real-time event insights and metrics
* **Broadcasts** - Mass messaging to guests
* **Support System** - Handle guest inquiries

### Authentication

Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

### Rate Limiting

API requests are rate-limited to ensure fair usage:
- **Per Minute**: 60 requests
- **Per Hour**: 1000 requests

### Environments

- **Development**: Full documentation and debugging enabled
- **Production**: Optimized for performance and security
"""

tags_metadata = [
    {
        "name": "Root",
        "description": "Root endpoints for API information and health checks",
    },
    {
        "name": "Health",
        "description": "Health check endpoints for monitoring and status verification",
    },
    {
        "name": "Authentication",
        "description": "User authentication, registration, and token management operations",
    },
    {
        "name": "Planners",
        "description": "Event planner profile management and settings",
    },
    {
        "name": "Events",
        "description": "Event creation, management, and lifecycle operations",
    },
    {
        "name": "Guests",
        "description": "Guest list management, RSVPs, and guest information",
    },
    {
        "name": "Conversations",
        "description": "WhatsApp conversation management and message history",
    },
    {
        "name": "Broadcasts",
        "description": "Mass messaging and broadcast campaign management",
    },
    {
        "name": "Support Requests",
        "description": "Guest support tickets and inquiry management",
    },
    {
        "name": "Analytics",
        "description": "Event analytics, metrics, and reporting",
    },
    {
        "name": "Webhooks",
        "description": "WhatsApp webhook endpoints for receiving messages and events",
    },
]

# Initialize FastAPI app with enhanced Swagger configuration
app = FastAPI(
    title="Eventsarthi API",
    description=description,
    version="1.0.0",
    terms_of_service="https://eventsarthi.com/terms",
    contact={
        "name": "Eventsarthi Support",
        "url": "https://eventsarthi.com/support",
        "email": "support@eventsarthi.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata,
    docs_url="/docs",  # Always enable Swagger UI
    redoc_url="/redoc",  # Always enable ReDoc
    openapi_url="/openapi.json",  # OpenAPI schema endpoint
    lifespan=lifespan,
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

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(TenantIsolationMiddleware)


# Exception Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled exceptions
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error" if settings.ENVIRONMENT == "production" else str(exc)
        }
    )


# Health Check Endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0"
    }


# Root Endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Welcome to Eventsarthi API",
        "version": "1.0.0",
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production",
        "health": "/health"
    }


# Include API Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(planners.router, prefix="/api/v1/planners", tags=["Planners"])
app.include_router(events.router, prefix="/api/v1/events", tags=["Events"])
app.include_router(guests.router, prefix="/api/v1/guests", tags=["Guests"])
app.include_router(conversations.router, prefix="/api/v1/conversations", tags=["Conversations"])
app.include_router(broadcasts.router, prefix="/api/v1/broadcasts", tags=["Broadcasts"])
app.include_router(support_requests.router, prefix="/api/v1/support-requests", tags=["Support Requests"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["Webhooks"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

# Made with Bob
