# Eventsarthi Backend

FastAPI backend for the Eventsarthi event management platform.
uvicorn app.main:app --reload
## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis

### Installation

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run with Docker Compose (Recommended)**
   ```bash
   docker-compose up -d
   ```

5. **Or run locally**
   ```bash
   # Start PostgreSQL and Redis first
   uvicorn app.main:app --reload
   ```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/v1/          # API routes
│   ├── core/            # Core utilities
│   ├── middleware/      # Custom middleware
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── utils/           # Helper functions
├── alembic/             # Database migrations
├── tests/               # Test suite
└── scripts/             # Utility scripts
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
isort app/
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Key Features

- **Multi-tenant Architecture**: Complete data isolation between planners
- **JWT Authentication**: Secure token-based authentication
- **WhatsApp Integration**: Webhook handling for WhatsApp messages
- **AI-Powered Bot**: Intelligent guest assistance
- **Rate Limiting**: Protection against abuse
- **Comprehensive Logging**: Request/response logging

## Environment Variables

See `.env.example` for all available configuration options.

## License

MIT