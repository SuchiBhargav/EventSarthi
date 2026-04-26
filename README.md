# Eventsarthi - AI-Powered Event Management Platform

> A comprehensive event management platform with WhatsApp integration, AI-powered guest assistance, and real-time planner coordination.

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Core Concepts](#core-concepts)
- [API Documentation](#api-documentation)
- [Security & Privacy](#security--privacy)
- [Deployment](#deployment)
- [Business Model](#business-model)
- [Contributing](#contributing)

## 🎯 Overview

Eventsarthi is an intelligent event management platform that connects event planners with guests through WhatsApp. It uses AI to provide personalized guest experiences, automate common queries, and streamline event coordination.

### Problem Statement

Traditional event management involves:
- Manual guest communication via multiple channels
- Repetitive queries about schedules, venues, and logistics
- Difficulty in personalizing communication for large guest lists
- Lack of real-time coordination between planners and guests

### Solution

Eventsarthi provides:
- **AI-Powered WhatsApp Bot** for instant guest assistance
- **Planner Dashboard** (Flutter mobile app) for event management
- **Intelligent Escalation** for complex requests
- **Personalized Messaging** based on guest profiles
- **Multi-tenant Architecture** ensuring complete data isolation

## ✨ Key Features

### For Guests (WhatsApp Interface)
- 🤖 **AI Assistant**: Instant answers to common questions
- 📍 **Venue Information**: Room numbers, hall locations, schedules
- 🍽️ **Food Preferences**: Dietary requirements and menu details
- 🚗 **Service Requests**: Cab booking, wheelchair assistance, etc.
- 📱 **Real-time Updates**: Event notifications and reminders

### For Planners (Flutter Mobile App)
- 📊 **Dashboard**: Real-time event overview and analytics
- 👥 **Guest Management**: Upload and manage guest lists
- 📢 **Broadcast Messages**: Send personalized bulk messages
- 🎫 **Request Management**: Handle guest service requests
- 📈 **Analytics**: Track engagement and attendance
- 🗺️ **Venue Mapping**: Upload hotel maps and room assignments

### AI Capabilities
- **Intent Recognition**: Understands guest queries and categorizes them
- **Context-Aware Responses**: Uses event-specific data (FAQ, schedule, guest info)
- **Personalization**: Adapts tone based on guest relationship and preferences
- **Smart Escalation**: Routes complex requests to planners
- **Multi-language Support**: English, Hindi, Kannada (extensible)

## 🏗️ Architecture

### System Components

```
┌─────────────────┐         ┌──────────────────┐
│  Guest (WhatsApp)│◄───────►│  WhatsApp Cloud  │
└─────────────────┘         │      API         │
                            └────────┬─────────┘
                                     │
                            ┌────────▼─────────┐
                            │   FastAPI        │
                            │   Backend        │
                            └────────┬─────────┘
                                     │
        ┌────────────────────────────┼────────────────────────┐
        │                            │                        │
┌───────▼────────┐      ┌───────────▼──────┐    ┌──────────▼────────┐
│   PostgreSQL   │      │      Redis       │    │   AI Service      │
│   + pgvector   │      │   (Upstash)      │    │  (GPT-4o-mini)    │
└────────────────┘      └──────────────────┘    └───────────────────┘
                                     │
                            ┌────────▼─────────┐
                            │  Planner App     │
                            │   (Flutter)      │
                            └──────────────────┘
```

### Data Flow

1. **Guest Query Flow**
   ```
   Guest → WhatsApp → Webhook → FastAPI → AI Service → Response
                                    ↓
                              Database Lookup
                                    ↓
                              Vector Search (FAQ)
   ```

2. **Planner Action Flow**
   ```
   Planner → Flutter App → API → Database → WhatsApp API → Guest
   ```

3. **Escalation Flow**
   ```
   Guest Query → AI (Low Confidence) → Create Ticket → Notify Planner
                                                            ↓
   Guest ← WhatsApp ← API ← Planner Response ← Planner App
   ```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+ with pgvector extension
- **Cache**: Redis (Upstash)
- **AI/ML**: OpenAI GPT-4o-mini / Google Gemini Flash
- **Message Queue**: Redis Queue (RQ) / Celery
- **Storage**: Cloudflare R2 / Supabase Storage

### Frontend
- **Mobile**: Flutter (Android + iOS)
- **State Management**: Riverpod / Bloc

### External Services
- **WhatsApp**: Meta WhatsApp Cloud API
- **Notifications**: Firebase Cloud Messaging
- **Monitoring**: Sentry / LogRocket

### DevOps
- **Hosting**: Render / Fly.io / Railway
- **CI/CD**: GitHub Actions
- **Containerization**: Docker

## 📁 Project Structure

```
Eventsarthi/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration management
│   │   ├── database.py             # Database connection
│   │   ├── dependencies.py         # Dependency injection
│   │   │
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── planner.py
│   │   │   ├── event.py
│   │   │   ├── guest.py
│   │   │   ├── conversation.py
│   │   │   ├── faq.py
│   │   │   ├── schedule.py
│   │   │   ├── broadcast.py
│   │   │   └── support_request.py
│   │   │
│   │   ├── schemas/                # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── planner.py
│   │   │   ├── event.py
│   │   │   ├── guest.py
│   │   │   ├── conversation.py
│   │   │   └── support_request.py
│   │   │
│   │   ├── api/                    # API routes
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── planners.py
│   │   │   │   ├── events.py
│   │   │   │   ├── guests.py
│   │   │   │   ├── conversations.py
│   │   │   │   ├── broadcasts.py
│   │   │   │   ├── support_requests.py
│   │   │   │   ├── analytics.py
│   │   │   │   └── webhooks.py
│   │   │
│   │   ├── services/               # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── planner_service.py
│   │   │   ├── event_service.py
│   │   │   ├── guest_service.py
│   │   │   ├── conversation_service.py
│   │   │   ├── ai_service.py
│   │   │   ├── whatsapp_service.py
│   │   │   ├── broadcast_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── personalization_service.py
│   │   │   ├── escalation_service.py
│   │   │   └── analytics_service.py
│   │   │
│   │   ├── core/                   # Core utilities
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   ├── cache.py
│   │   │   ├── vector_store.py
│   │   │   ├── queue.py
│   │   │   └── storage.py
│   │   │
│   │   ├── middleware/             # Custom middleware
│   │   │   ├── __init__.py
│   │   │   ├── tenant_isolation.py
│   │   │   ├── rate_limiting.py
│   │   │   └── logging.py
│   │   │
│   │   └── utils/                  # Helper functions
│   │       ├── __init__.py
│   │       ├── validators.py
│   │       ├── formatters.py
│   │       └── constants.py
│   │
│   ├── alembic/                    # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── tests/                      # Test suite
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_api/
│   │   ├── test_services/
│   │   └── test_models/
│   │
│   ├── scripts/                    # Utility scripts
│   │   ├── seed_data.py
│   │   ├── cleanup_old_events.py
│   │   └── migrate_data.py
│   │
│   ├── requirements.txt            # Python dependencies
│   ├── requirements-dev.txt        # Development dependencies
│   ├── .env.example                # Environment variables template
│   ├── Dockerfile                  # Docker configuration
│   ├── docker-compose.yml          # Docker Compose setup
│   └── README.md                   # Backend documentation
│
├── mobile/                         # Flutter mobile app
│   └── (Flutter project structure)
│
├── docs/                           # Documentation
│   ├── API.md
│   ├── DEPLOYMENT.md
│   ├── ARCHITECTURE.md
│   └── CONTRIBUTING.md
│
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       └── mobile-ci.yml
│
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis
- Flutter SDK (for mobile app)
- WhatsApp Business Account

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/eventsarthi.git
   cd eventsarthi/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   alembic upgrade head
   python scripts/seed_data.py  # Optional: seed test data
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

   API will be available at `http://localhost:8000`
   API docs at `http://localhost:8000/docs`

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/eventsarthi
REDIS_URL=redis://localhost:6379

# WhatsApp
WHATSAPP_API_TOKEN=your_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_verify_token

# AI Service
OPENAI_API_KEY=your_openai_key
# OR
GEMINI_API_KEY=your_gemini_key

# Storage
CLOUDFLARE_R2_ACCESS_KEY=your_key
CLOUDFLARE_R2_SECRET_KEY=your_secret
CLOUDFLARE_R2_BUCKET=your_bucket

# Security
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App Settings
ENVIRONMENT=development
DEBUG=true
```

## 💡 Core Concepts

### 1. Multi-Tenant Architecture

**Critical Rule**: Every table MUST include `planner_id` and `event_id` to ensure complete data isolation.

```sql
-- Example: guests table
CREATE TABLE guests (
    guest_id UUID PRIMARY KEY,
    planner_id UUID NOT NULL,  -- Ensures tenant separation
    event_id UUID NOT NULL,    -- Ensures event separation
    name VARCHAR(255),
    phone VARCHAR(20),
    -- ... other fields
    FOREIGN KEY (planner_id) REFERENCES planners(planner_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);
```

**Query Pattern** (Always filter by both IDs):
```python
# ❌ Wrong
guest = db.query(Guest).filter(Guest.phone == phone).first()

# ✅ Correct
guest = db.query(Guest).filter(
    Guest.planner_id == planner_id,
    Guest.event_id == event_id,
    Guest.phone == phone
).first()
```

### 2. AI Bot Decision Flow

```
Guest Query
    ↓
Intent Classification
    ↓
┌───────────────────────────────────┐
│ Can answer from knowledge?        │
│ (FAQ, Schedule, Guest Profile)    │
└───────┬───────────────────────────┘
        │
    ┌───▼───┐
    │  YES  │ → Generate Response → Send to Guest
    └───────┘
        │
    ┌───▼───┐
    │   NO  │ → Is it an action request?
    └───┬───┘
        │
    ┌───▼───────────────────────────┐
    │ Action Request?               │
    │ (Cab, Wheelchair, Help)       │
    └───────┬───────────────────────┘
            │
        ┌───▼───┐
        │  YES  │ → Create Support Ticket → Notify Planner
        └───────┘
            │
        ┌───▼───┐
        │   NO  │ → Low Confidence / Unknown → Escalate to Planner
        └───────┘
```

### 3. Escalation Rules

Bot MUST escalate if:
- ❌ Question not found in FAQ and confidence < threshold
- ❌ Involves money/payment
- ❌ Involves health/medical issues
- ❌ Involves transport booking
- ❌ Involves room change / hotel management
- ❌ Guest is angry or uses emergency keywords
- ❌ Guest asks something personal

### 4. Personalized Messaging

Messages are personalized based on:
- **Relation Type**: Uncle/Aunt (respectful) vs Friend (casual)
- **Language**: English, Hindi, Kannada
- **Health Notes**: Diabetes → mention sugar-free options
- **VIP Level**: Special treatment for VIP guests

**Example Templates**:

```python
# For Uncle (Respectful)
"Namaste {{name}} ji 🙏
Sangeet has started. We would love to see you join us.
Also, we have arranged sugar-free dessert options for you."

# For Friend (Casual)
"Hey {{name}} bro 😄🔥
Sangeet is live! You coming or what?
Event starts in 20 mins, jaldi aa!"
```

### 5. Data Retention & Privacy

**After Event Completion**:
- ✅ Keep full data for **30 days**
- ✅ After 30 days, delete:
  - Guest phone numbers
  - Room numbers
  - Meal preferences
  - Chat history
- ✅ Keep (anonymized):
  - Event metadata
  - Analytics summary
  - Question statistics

## 📚 API Documentation

### Authentication

All planner endpoints require JWT authentication:
```
Authorization: Bearer <token>
```

### Key Endpoints

#### Planner Management
- `POST /api/v1/auth/register` - Register new planner
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/planners/me` - Get current planner profile

#### Event Management
- `POST /api/v1/events` - Create event
- `GET /api/v1/events/{event_id}` - Get event details
- `PUT /api/v1/events/{event_id}` - Update event
- `DELETE /api/v1/events/{event_id}` - Delete event

#### Guest Management
- `POST /api/v1/events/{event_id}/guests` - Add guests (bulk upload)
- `GET /api/v1/events/{event_id}/guests` - List guests
- `PUT /api/v1/guests/{guest_id}` - Update guest
- `DELETE /api/v1/guests/{guest_id}` - Remove guest

#### Broadcasts
- `POST /api/v1/events/{event_id}/broadcasts` - Send broadcast message
- `GET /api/v1/events/{event_id}/broadcasts` - List broadcasts

#### Support Requests
- `GET /api/v1/events/{event_id}/support-requests` - List requests
- `PUT /api/v1/support-requests/{request_id}` - Update request status
- `POST /api/v1/support-requests/{request_id}/reply` - Reply to guest

#### WhatsApp Webhook
- `POST /api/v1/webhooks/whatsapp` - Receive WhatsApp messages
- `GET /api/v1/webhooks/whatsapp` - Verify webhook

Full API documentation available at `/docs` (Swagger UI)

## 🔒 Security & Privacy

### Authentication & Authorization
- **Planners**: JWT-based authentication
- **Guests**: Phone number verification via WhatsApp
- **API Keys**: Secure storage in environment variables

### Data Protection
- ✅ Encrypt phone numbers and room numbers at rest
- ✅ TLS/HTTPS for all communications
- ✅ Row-Level Security (RLS) in PostgreSQL
- ✅ Rate limiting on all endpoints
- ✅ Input validation and sanitization

### Audit Logging
Track all sensitive operations:
- Planner broadcasts
- Guest data changes
- Bot responses (for debugging)
- Support request handling

### Privacy Compliance
- GDPR-compliant data retention
- Right to deletion
- Data export capabilities
- Transparent privacy policy

## 🚢 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Checklist

- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=false`
- [ ] Use strong `JWT_SECRET_KEY`
- [ ] Configure SSL/TLS certificates
- [ ] Set up database backups
- [ ] Configure monitoring (Sentry)
- [ ] Set up log aggregation
- [ ] Configure rate limiting
- [ ] Enable CORS for mobile app domain
- [ ] Set up CDN for static assets
- [ ] Configure auto-scaling

### Recommended Hosting

- **Backend**: Render, Fly.io, or Railway
- **Database**: Supabase, Neon, or managed PostgreSQL
- **Redis**: Upstash
- **Storage**: Cloudflare R2 or Supabase Storage

## 💰 Business Model

### Pricing Tiers

#### Free Tier
- 1 event
- Up to 200 guests
- Limited broadcasts (50/month)
- Basic AI responses
- 7-day data retention

#### Pro Tier ($49/event)
- Unlimited guests
- Unlimited broadcasts
- Advanced personalization
- Analytics dashboard
- 30-day data retention
- Priority support

#### Enterprise Tier (Custom)
- Multi-language bot
- Custom integrations
- Dedicated support
- 90-day data retention
- White-label option
- Voice bot (future)
- Hotel booking system integration

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- Follow PEP 8 for Python code
- Write unit tests for new features
- Update documentation
- Use type hints
- Add docstrings to functions

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Email**: support@eventsarthi.com
- **Documentation**: https://docs.eventsarthi.com
- **Issues**: https://github.com/yourusername/eventsarthi/issues

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- OpenAI for AI capabilities
- Meta for WhatsApp Cloud API
- Flutter team for the mobile framework

---

**Built with ❤️ for event planners and their guests**
