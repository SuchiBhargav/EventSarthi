# Eventsarthi - Project Flow & Technical Documentation

## 📑 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture & Data Flow](#architecture--data-flow)
3. [Code Structure & Modules](#code-structure--modules)
4. [Database Models](#database-models)
5. [API Endpoints](#api-endpoints)
6. [Core Services](#core-services)
7. [Authentication & Security](#authentication--security)
8. [WhatsApp Integration Flow](#whatsapp-integration-flow)
9. [AI Bot Decision Flow](#ai-bot-decision-flow)
10. [Testing Guide](#testing-guide)
11. [Development Workflow](#development-workflow)
12. [Deployment Guide](#deployment-guide)

---

## 🎯 Project Overview

**Eventsarthi** is an AI-powered event management platform that connects event planners with guests through WhatsApp. It provides intelligent guest assistance, automated responses, and real-time coordination.

### Key Components
- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+ with pgvector
- **Cache**: Redis (Upstash)
- **AI**: OpenAI GPT-4o-mini / Google Gemini Flash
- **Messaging**: WhatsApp Cloud API
- **Mobile**: Flutter (separate repository)

### 🎯 Planner Interface Strategy

**Important**: Planners use **TWO interfaces** for different purposes:

#### 📱 Flutter/Web App (For Setup & Analytics)
Used **BEFORE and AFTER** the event for:
- ✅ Upload documents (menu, guest list, venue maps, schedules)
- ✅ Bulk import guests from CSV/Excel
- ✅ Configure event settings and FAQs
- ✅ View analytics and engagement statistics
- ✅ Review chat history and conversation logs
- ✅ Generate reports on guest interactions

#### 💬 WhatsApp Bot (For Real-Time Event Management)
Used **DURING the event** for:
- ✅ Receive escalation notifications instantly
- ✅ View guest details when escalation occurs
- ✅ Reply to guest queries directly via WhatsApp
- ✅ Send scheduled notifications to all guests
- ✅ Handle urgent requests on-the-go
- ✅ Quick access without opening app

**Why This Approach?**
- During events, planners are busy and need **instant notifications**
- WhatsApp is always accessible on their phone
- No need to open app repeatedly to check for issues
- Faster response time for guest escalations
- Planner can manage event while moving around venue


---

## 🏗️ Architecture & Data Flow

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GUEST INTERACTION                        │
│                                                              │
│  Guest → WhatsApp → Meta Cloud API → Webhook → FastAPI     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND PROCESSING                        │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  Middleware  │ → │   API Routes  │ → │   Services   │ │
│  │  - Logging   │    │  - Auth       │    │  - AI        │ │
│  │  - Rate Limit│    │  - Events     │    │  - WhatsApp  │ │
│  │  - Tenant    │    │  - Guests     │    │  - Broadcast │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  PostgreSQL  │    │    Redis     │    │  AI Service  │ │
│  │  + pgvector  │    │   (Cache)    │    │  (OpenAI)    │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    PLANNER INTERFACE                         │
│                                                              │
│  Planner ← Flutter App ← REST API ← FastAPI Backend        │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow Diagrams

#### 1. Guest Message Flow
```
Guest sends WhatsApp message
    ↓
WhatsApp Cloud API receives message
    ↓
Webhook POST to /api/v1/webhooks/whatsapp
    ↓
Middleware Processing:
    - Logging (LoggingMiddleware)
    - Rate Limiting (RateLimitMiddleware)
    - Tenant Isolation (TenantIsolationMiddleware)
    ↓
Webhook Handler:
    - Verify signature
    - Extract message data
    - Identify guest by phone number
    ↓
AI Service Processing:
    - Classify intent
    - Search FAQ (vector search)
    - Check guest profile
    - Generate response
    ↓
Decision:
    ├─ Can Answer? → Send response via WhatsApp API
    ├─ Action Request? → Create support ticket → Notify planner

#### 3. Planner WhatsApp Bot Flow (Real-Time Event Management)
```
Escalation occurs (guest needs help)
    ↓
System sends WhatsApp message to Planner:
    "🚨 Escalation Alert
    Guest: Rajesh Kumar (Uncle)
    Room: 305
    Issue: Need wheelchair assistance
    Reply to this message to respond"
    ↓
Planner replies via WhatsApp:
    "We're sending wheelchair to room 305 now"
    ↓
Backend receives planner's WhatsApp message
    ↓
Webhook identifies it's from planner (not guest)
    ↓
Extract escalation context from conversation thread
    ↓
Update support ticket status to "resolved"
    ↓
Send planner's response to guest via WhatsApp
    ↓
Guest receives: "We're sending wheelchair to room 305 now"
    ↓
Log interaction in database
```

#### 4. Scheduled Notification Flow
```
Planner schedules notification via Flutter app:
    - Message: "Sangeet ceremony starting in 30 mins"
    - Schedule: 7:30 PM
    - Target: All attending guests
    ↓
System stores scheduled broadcast in database
    ↓
Background job checks for pending broadcasts every minute
    ↓
At 7:30 PM, job triggers broadcast service
    ↓
Broadcast service:
    - Fetches all attending guests
    - Personalizes message per guest
    - Sends in batches of 50
    - 1 second delay between batches
    ↓
WhatsApp API sends messages to all guests
    ↓
Track delivery status in database
    ↓
Planner receives confirmation via WhatsApp:
    "✅ Broadcast sent to 150 guests"
```

    └─ Low Confidence? → Escalate to planner
    ↓
Store conversation in database
    ↓
Return 200 OK to WhatsApp
```

#### 2. Planner Action Flow
```
Planner opens Flutter app
    ↓
Login: POST /api/v1/auth/login
    ↓
Receive JWT token
    ↓
Fetch events: GET /api/v1/events
    ↓
View guests: GET /api/v1/events/{event_id}/guests
    ↓
Send broadcast: POST /api/v1/events/{event_id}/broadcasts
    ↓
Broadcast Service:
    - Personalize messages per guest
    - Batch processing (50 guests/batch)
    - Send via WhatsApp API
    - Track delivery status
    ↓
Update database with broadcast status
```

---

## 📂 Code Structure & Modules

### Directory Structure
```
backend/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Configuration management
│   ├── database.py              # Database connection & session
│   ├── dependencies.py          # Dependency injection functions
│   │
│   ├── api/v1/                  # API Routes
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── planners.py          # Planner management
│   │   ├── events.py            # Event CRUD
│   │   ├── guests.py            # Guest management
│   │   ├── conversations.py     # Chat history
│   │   ├── broadcasts.py        # Bulk messaging
│   │   ├── support_requests.py  # Ticket system
│   │   ├── analytics.py         # Analytics & reports
│   │   └── webhooks.py          # WhatsApp webhooks
│   │
│   ├── models/                  # SQLAlchemy ORM Models
│   │   ├── planner.py           # Planner model
│   │   ├── event.py             # Event model
│   │   ├── guest.py             # Guest model
│   │   ├── conversation.py      # Message history
│   │   ├── faq.py               # FAQ knowledge base
│   │   ├── schedule.py          # Event schedule
│   │   ├── broadcast.py         # Broadcast campaigns
│   │   └── support_request.py   # Support tickets
│   │
│   ├── schemas/                 # Pydantic Schemas
│   ├── services/                # Business Logic Layer
│   ├── core/                    # Core Utilities
│   ├── middleware/              # Custom Middleware
│   └── utils/                   # Helper Functions
│
├── alembic/                     # Database Migrations
├── tests/                       # Test Suite
├── scripts/                     # Utility Scripts
└── requirements.txt             # Python dependencies
```

### Key Module Responsibilities

#### **main.py** - Application Entry Point
- Initialize FastAPI app
- Configure middleware (CORS, logging, rate limiting, tenant isolation)
- Register API routers
- Setup lifespan events (startup/shutdown)
- Global exception handling
- Health check endpoint

#### **config.py** - Configuration Management
- Load environment variables using Pydantic Settings
- Database, Redis, WhatsApp, AI service configurations
- Security settings (JWT, CORS)
- Feature flags and limits


### Planner Use Cases

#### Use Case 1: Pre-Event Setup (Flutter/Web App)
```
Day 1-7 before event:
1. Planner logs into Flutter app
2. Creates new event with details
3. Uploads guest list (CSV with 200 guests)
4. Uploads venue map (hotel floor plan)
5. Adds FAQs:
   - "What time is sangeet?" → "7 PM at Grand Ballroom"
   - "Where is parking?" → "Basement level B1 and B2"
6. Configures event schedule
7. Sets up room assignments
8. Reviews analytics dashboard (0 interactions yet)
```

#### Use Case 2: During Event (WhatsApp Bot)
```
Event Day - 6:30 PM:
Planner is at venue coordinating

6:35 PM - Receives WhatsApp:
"🚨 Escalation from Amit Shah (Friend)
Room: 402
Message: 'AC not working in my room, it's too hot'
Reply to respond"

Planner replies immediately:
"I'll send maintenance to room 402 right away"

6:37 PM - Maintenance dispatched
Guest receives planner's message

7:00 PM - Planner sends via WhatsApp:
"Send notification: Sangeet starting in 30 mins"

System broadcasts to all 200 guests with personalization

7:15 PM - Another escalation:
"🚨 Escalation from Mrs. Sharma (Aunt)
Room: 305
Message: 'Need wheelchair for my husband'
Reply to respond"

Planner replies:
"Wheelchair being sent to room 305 immediately"

8:00 PM - Planner checks status via WhatsApp:
"Show escalations"

Bot replies:
"✅ 2 resolved
⏳ 1 pending (cab booking for tomorrow)"
```

#### Use Case 3: Post-Event Analytics (Flutter/Web App)
```
Day after event:
1. Planner opens Flutter app
2. Views analytics dashboard:
   - Total messages: 450
   - Bot handled: 380 (84%)
   - Escalations: 70 (16%)
   - Most asked: "What time is dinner?" (45 times)
   - Average response time: 2 seconds
3. Reviews conversation logs
4. Exports data for future events
5. Archives event (data retained for 30 days)
```

#### **database.py** - Database Layer
- SQLAlchemy engine creation with connection pooling
- Session management with `get_db()` dependency
- Database initialization functions

#### **dependencies.py** - Dependency Injection
- `get_current_planner()` - Extract planner from JWT token
- `verify_event_access()` - Check planner owns event
- `PaginationParams` - Pagination helper class
- `verify_whatsapp_webhook()` - Webhook verification

---

## 🗄️ Database Models

### Entity Relationship Diagram

```
┌─────────────────┐
│    Planner      │
│  (Tenant Root)  │
└────────┬────────┘
         │ 1:N
         ↓
┌─────────────────┐
│     Event       │
│  planner_id FK  │
└────────┬────────┘

### Flutter/Web App Features (Setup & Analytics Only)

#### 📤 Upload & Configuration Features
```
1. Event Setup
   - Create/edit event details
   - Set dates, venue, timings
   - Configure bot settings

2. Guest Management
   - Bulk upload CSV/Excel (name, phone, room, relation, preferences)
   - Manual add/edit individual guests
   - Assign room numbers
   - Set VIP levels and dietary preferences

3. Document Uploads
   - Event menu (PDF)
   - Venue maps (images)
   - Hotel floor plans
   - Schedule documents

4. FAQ Management
   - Add common questions and answers
   - Categorize (venue, food, schedule, transport)
   - System auto-generates embeddings for AI search

5. Schedule Configuration
   - Add event timeline (Sangeet 7 PM, Dinner 9 PM, etc.)
   - Set reminders and notifications
   - Configure auto-notifications

6. Broadcast Setup
   - Create message templates
   - Schedule future broadcasts
   - Set target filters (VIP only, specific rooms, etc.)
```

#### 📊 Analytics & Reporting Features
```
1. Dashboard Overview
   - Total guests vs checked-in
   - Messages handled by bot vs escalated
   - Response time metrics
   - Engagement rate

2. Conversation Analytics
   - Most asked questions
   - Peak messaging times
   - Guest satisfaction indicators
   - Bot confidence scores

3. Guest Engagement
   - Individual guest interaction history
   - Message read/delivery status
   - Response patterns

4. Escalation Reports
   - Total escalations by category
   - Average resolution time
   - Pending vs resolved tickets

5. Export Options
   - Download conversation logs (CSV)
   - Export analytics reports (PDF)
   - Guest interaction summary
```

**Important**: The Flutter/Web app does NOT handle real-time messaging during events. That's done via WhatsApp bot for instant access.

         │ 1:N
         ├──────────────────┬──────────────┬──────────────┬──────────────┐
         ↓                  ↓              ↓              ↓              ↓
┌─────────────┐    ┌─────────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
│   Guest     │    │     FAQ     │  │ Schedule │  │Broadcast │  │SupportRequest│
│ planner_id  │    │ planner_id  │  │planner_id│  │planner_id│  │  planner_id  │
│ event_id FK │    │ event_id FK │  │event_id  │  │event_id  │  │  event_id FK │
└──────┬──────┘    └─────────────┘  └──────────┘  └──────────┘  └──────┬───────┘
       │ 1:N                                                             │
       └────────────────────────────┬────────────────────────────────────┘
                                    ↓
                            ┌───────────────┐
                            │ Conversation  │
                            │  planner_id   │
                            │  event_id FK  │
                            │  guest_id FK  │
                            └───────────────┘
```

### Critical: Multi-Tenant Architecture

**Every table MUST include `planner_id` and `event_id` for complete data isolation.**

```python
# ❌ WRONG - Security vulnerability
guest = db.query(Guest).filter(Guest.phone == phone).first()

# ✅ CORRECT - Tenant isolated
guest = db.query(Guest).filter(
    Guest.planner_id == current_planner.planner_id,
    Guest.event_id == event_id,
    Guest.phone == phone
).first()
```

### Key Models

#### 1. Planner (Tenant Root)
```python
planner_id (UUID, PK)
email (unique)
phone (unique)
password_hash
full_name
company_name
subscription_tier (free/pro/enterprise)
is_active
max_events, max_guests_per_event
created_at, updated_at
```

### Planner WhatsApp Bot Commands

The planner can interact with the system via WhatsApp using simple commands:

```
Available Commands:

1. "Show escalations" or "Pending issues"
   → Lists all pending support requests

2. "Show stats" or "Event status"
   → Quick statistics (guests checked in, messages today, etc.)

3. "Send notification: [message]"
   → Broadcasts message to all guests immediately

4. "Schedule: [time] - [message]"
   → Schedules notification for specific time

5. Reply to escalation message
   → Automatically responds to the guest who raised the issue

6. "Guest info: [name or phone]"
   → Shows guest details (room, preferences, etc.)

7. "Help"
   → Shows available commands
```

**Example Interactions:**

```
Planner: "Show escalations"
Bot: "📋 Pending Escalations:
1. Rajesh Kumar - Need cab at 6 AM
2. Priya Sharma - Room AC issue
3. Amit Patel - Dietary concern
Reply with number to view details"

Planner: "1"
Bot: "🚕 Cab Request
Guest: Rajesh Kumar (Uncle)
Room: 402
Phone: +91 98765 43210
Request: Need cab to airport at 6 AM tomorrow
Reply to this message to respond"

Planner: "Cab booked for 6 AM. Driver will call you at 5:45 AM"
Bot: "✅ Response sent to Rajesh Kumar
Ticket marked as resolved"
```


#### 2. Event
```python
event_id (UUID, PK)
planner_id (UUID, FK) ← CRITICAL
event_name
event_type (wedding/corporate/birthday)
start_date, end_date
venue_name, venue_address
status (DRAFT/ACTIVE/COMPLETED/ARCHIVED)
bot_enabled
total_guests
```

#### 3. Guest
```python
guest_id (UUID, PK)
planner_id (UUID, FK) ← CRITICAL
event_id (UUID, FK) ← CRITICAL
name, phone, email
relation_type (uncle/aunt/friend/vip)
tone_preference (formal/casual/respectful)
language (en/hi/kn)
vip_level
health_notes (JSON: diabetes, allergies)
food_preference
hotel_name, room_number
is_attending, checked_in
```

---

## 🔌 API Endpoints

### Authentication (`/api/v1/auth`)
```
POST   /register          - Register new planner
POST   /login             - Login and get JWT token
POST   /refresh           - Refresh access token
POST   /logout            - Logout current planner
POST   /verify-email      - Verify email address
POST   /forgot-password   - Request password reset
POST   /reset-password    - Reset password with token
```

### Events (`/api/v1/events`)
```
POST   /                  - Create new event
GET    /                  - List all events for planner
GET    /{event_id}        - Get event details
PUT    /{event_id}        - Update event
DELETE /{event_id}        - Delete event
POST   /{event_id}/faqs   - Add FAQ to event
```

### Guests (`/api/v1/guests`)
```
POST   /events/{event_id}/guests  - Add guests (bulk upload)
GET    /events/{event_id}/guests  - List guests
GET    /guests/{guest_id}         - Get guest details
PUT    /guests/{guest_id}         - Update guest
DELETE /guests/{guest_id}         - Remove guest
```

### Broadcasts (`/api/v1/broadcasts`)
```
POST   /events/{event_id}/broadcasts  - Send broadcast message
GET    /events/{event_id}/broadcasts  - List broadcasts
GET    /broadcasts/{id}/stats         - Get delivery stats
```

### Webhooks (`/api/v1/webhooks`)
```
GET    /whatsapp          - Verify webhook (WhatsApp setup)
POST   /whatsapp          - Receive WhatsApp messages
```

---

## ⚙️ Core Services

### 1. AI Service (`ai_service.py`)
**Purpose**: Handles all AI/LLM interactions

**Key Functions**:
```python
classify_intent(message: str) -> Intent
    # Classifies user message into categories
    # Returns: question, request, greeting, complaint

generate_response(message: str, context: dict) -> str
    # Generates AI response using GPT-4o-mini
    # Context includes: guest profile, FAQ, schedule

search_faq(query: str, event_id: str) -> List[FAQ]
    # Semantic search using vector embeddings
    # Returns top 3 relevant FAQs

should_escalate(message: str, confidence: float) -> bool
    # Determines if query should be escalated
    # Rules: low confidence, payment, medical, angry tone
```

### 2. WhatsApp Service (`whatsapp_service.py`)
**Purpose**: WhatsApp Cloud API integration

**Key Functions**:
```python
send_message(phone: str, message: str) -> bool
send_template_message(phone: str, template: str, params: dict)
send_media(phone: str, media_url: str, caption: str)
verify_webhook_signature(payload: bytes, signature: str) -> bool
```

### 3. Broadcast Service (`broadcast_service.py`)
**Purpose**: Bulk messaging with personalization

**Key Functions**:
```python
send_broadcast(event_id: str, message_template: str, filters: dict)
    # Sends personalized messages to filtered guests
    # Processes in batches of 50
    # Applies rate limiting (1 sec delay between batches)

personalize_message(template: str, guest: Guest) -> str
    # Replaces {{name}}, {{room_number}} etc.
    # Adjusts tone based on relation_type
```

---

## 🔐 Authentication & Security

### JWT Token Flow

```python
# Token Structure
{
    "sub": "planner_id",           # Subject (planner UUID)
    "email": "planner@example.com",
    "exp": 1234567890,             # Expiration timestamp
    "type": "access"               # Token type
}

# Token Generation (security.py)
def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

# Token Verification (dependencies.py)
def get_current_planner(credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    planner_id = payload.get("sub")
    planner = db.query(Planner).filter(Planner.planner_id == planner_id).first()
    return planner
```

### Rate Limiting
- 60 requests per minute per IP
- 1000 requests per hour per IP
- Uses Redis for distributed rate limiting
- Returns 429 Too Many Requests if exceeded

---

## 📱 WhatsApp Integration Flow

### Message Processing Pipeline

```python
# 1. Receive webhook
webhook_data = await request.json()

# 2. Verify signature
verify_webhook_signature(webhook_data, signature)

# 3. Extract message
message = extract_message(webhook_data)
phone = message["from"]
text = message["text"]["body"]

# 4. Identify guest
guest = db.query(Guest).filter(
    Guest.phone == phone,
    Guest.whatsapp_opted_in == True
).first()

# 5. AI Processing
intent = ai_service.classify_intent(text)
response = ai_service.generate_response(text, context)
confidence = ai_service.calculate_confidence(response)

# 6. Decision
if confidence > 0.7:
    whatsapp_service.send_message(phone, response)
else:
    escalation_service.create_support_ticket(guest.guest_id, text)

# 7. Store conversation
conversation = Conversation(...)
db.add(conversation)
db.commit()
```

---

## 🤖 AI Bot Decision Flow

### Intent Classification

```python
INTENTS = {
    "question": ["what", "when", "where", "how", "time", "location"],
    "request": ["need", "want", "book", "arrange", "cab", "wheelchair"],
    "greeting": ["hi", "hello", "hey", "namaste"],
    "complaint": ["problem", "issue", "angry", "disappointed"]
}
```

### Escalation Rules

```python
def should_escalate(message: str, confidence: float, guest: Guest) -> bool:
    # Rule 1: Low confidence
    if confidence < 0.7:
        return True
    
    # Rule 2: Payment/money keywords
    if any(word in message.lower() for word in ["pay", "payment", "money"]):
        return True
    
    # Rule 3: Medical/health keywords
    if any(word in message.lower() for word in ["doctor", "medical", "emergency"]):
        return True
    
    # Rule 4: VIP guests
    if guest.vip_level == "vip":
        return True
    
    return False
```

---

## 🧪 Testing Guide

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api/test_auth.py

# Run with verbose output
pytest -v
```

### Test Example

```python
# tests/test_api/test_events.py
def test_create_event(client, auth_token):
    response = client.post(
        "/api/v1/events",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "event_name": "Test Wedding",
            "event_type": "wedding",
            "start_date": "2024-12-01T10:00:00",
            "end_date": "2024-12-03T22:00:00"
        }
    )
    assert response.status_code == 201
    assert response.json()["event_name"] == "Test Wedding"
```

---

## 🔄 Development Workflow

### Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/eventsarthi.git
cd eventsarthi/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start services
docker-compose up -d postgres redis

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Making Changes

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and format code
black app/
isort app/

# Run tests
pytest

# Commit and push
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

---

## 🚀 Deployment Guide

### Docker Deployment

```bash
# Build image
docker build -t eventsarthi-backend:latest .

# Run container
docker run -d \
  --name eventsarthi-backend \
  -p 8000:8000 \
  --env-file .env \
  eventsarthi-backend:latest
```

### Health Check

```bash
curl https://api.eventsarthi.com/health

# Expected response:
{
  "status": "healthy",
  "environment": "production",
  "version": "1.0.0"
}
```

---

## 📝 Summary

This documentation covers:
- ✅ Complete architecture and data flow
- ✅ Code structure and module organization
- ✅ Database models with multi-tenant architecture
- ✅ API endpoints and their purposes
- ✅ Core services and their functions
- ✅ Authentication and security patterns
- ✅ WhatsApp integration flow
- ✅ AI bot decision logic
- ✅ Testing guidelines and examples
- ✅ Development workflow
- ✅ Deployment instructions

For more details, refer to:
- Main README.md for project overview
- API documentation at `/docs` endpoint
- Individual module docstrings in code

---

**Built with ❤️ for Eventsarthi**