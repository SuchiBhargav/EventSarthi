#!/usr/bin/env python3
"""
Script to create a test user for development
"""
import sys
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models.planner import Planner
from app.core.security import get_password_hash

def create_test_user():
    db = SessionLocal()
    try:
        # Check existing users
        planners = db.query(Planner).all()
        print(f"Found {len(planners)} existing planners:")
        for p in planners:
            print(f"  - Phone: {p.phone}, Email: {p.email}")
        
        # Check if test user exists
        test_phone = "+919876543210"
        existing = db.query(Planner).filter(Planner.phone == test_phone).first()
        
        if existing:
            print(f"\nTest user already exists with phone: {test_phone}")
            print(f"Email: {existing.email}")
            print("You can login with this phone number and password: 'password123'")
        else:
            # Create test user
            test_user = Planner(
                email="test@eventsarthi.com",
                phone=test_phone,
                password_hash=get_password_hash("password123"),
                full_name="Test Planner",
                company_name="Test Events",
                is_active=True,
                is_verified=True,
                email_verified=True,
                phone_verified=True,
            )
            db.add(test_user)
            db.commit()
            print(f"\n✅ Test user created successfully!")
            print(f"Phone: {test_phone}")
            print(f"Email: test@eventsarthi.com")
            print(f"Password: password123")
            print("\nYou can now login with these credentials.")
    
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()

# Made with Bob
