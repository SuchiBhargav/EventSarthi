"""
Application Constants
"""

# Event Types
EVENT_TYPES = [
    "wedding",
    "corporate",
    "birthday",
    "anniversary",
    "conference",
    "party",
    "other"
]

# Relation Types
RELATION_TYPES = [
    "uncle",
    "aunt",
    "friend",
    "cousin",
    "colleague",
    "family",
    "vip",
    "other"
]

# Food Preferences
FOOD_PREFERENCES = [
    "veg",
    "non-veg",
    "vegan",
    "jain",
    "no-preference"
]

# VIP Levels
VIP_LEVELS = [
    "regular",
    "vip",
    "close",
    "casual"
]

# Support Request Categories
REQUEST_CATEGORIES = [
    "transport",
    "help",
    "food",
    "medical",
    "accommodation",
    "venue_query",
    "unknown"
]

# Request Priorities
REQUEST_PRIORITIES = [
    "low",
    "normal",
    "high",
    "urgent"
]

# Languages
SUPPORTED_LANGUAGES = [
    "en",  # English
    "hi",  # Hindi
    "kn"   # Kannada
]

# Message Templates
GREETING_TEMPLATES = {
    "en": "Hello {name}! Welcome to {event_name}.",
    "hi": "नमस्ते {name}! {event_name} में आपका स्वागत है।",
    "kn": "ನಮಸ್ಕಾರ {name}! {event_name} ಗೆ ಸ್ವಾಗತ."
}

# Escalation Keywords
ESCALATION_KEYWORDS = [
    "urgent",
    "emergency",
    "help",
    "problem",
    "issue",
    "complaint",
    "angry",
    "disappointed"
]

# AI Intent Categories
AI_INTENTS = [
    "greeting",
    "schedule_query",
    "venue_query",
    "food_query",
    "accommodation_query",
    "transport_request",
    "help_request",
    "feedback",
    "unknown"
]

# Made with Bob
