"""
Planner Management Routes
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.dependencies import get_current_planner
from app.models.planner import Planner

router = APIRouter()


class PlannerUpdate(BaseModel):
    """Schema for updating planner profile"""

    full_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    whatsapp_number: Optional[str] = None
    language_preference: Optional[str] = None
    timezone: Optional[str] = None


@router.get("/me")
async def get_current_planner_profile(
    current_planner: Planner = Depends(get_current_planner),
):
    """Get current planner profile"""
    return {
        "planner_id": str(current_planner.planner_id),
        "email": current_planner.email,
        "phone": current_planner.phone,
        "full_name": current_planner.full_name,
        "company_name": current_planner.company_name,
        "profile_image_url": current_planner.profile_image_url,
        "whatsapp_number": current_planner.whatsapp_number,
        "is_active": current_planner.is_active,
        "is_verified": current_planner.is_verified,
        "email_verified": current_planner.email_verified,
        "phone_verified": current_planner.phone_verified,
        "subscription_tier": current_planner.subscription_tier,
        "language_preference": current_planner.language_preference,
        "timezone": current_planner.timezone,
        "created_at": current_planner.created_at,
        "last_login_at": current_planner.last_login_at,
    }


@router.put("/me")
async def update_planner_profile(
    profile_data: PlannerUpdate,
    current_planner: Planner = Depends(get_current_planner),
    db: Session = Depends(get_db),
):
    """Update planner profile"""
    if profile_data.full_name is not None:
        current_planner.full_name = profile_data.full_name  # type: ignore[assignment]
    if profile_data.company_name is not None:
        current_planner.company_name = profile_data.company_name  # type: ignore[assignment]
    if profile_data.phone is not None:
        current_planner.phone = profile_data.phone  # type: ignore[assignment]
    if profile_data.whatsapp_number is not None:
        current_planner.whatsapp_number = profile_data.whatsapp_number  # type: ignore[assignment]
    if profile_data.language_preference is not None:
        current_planner.language_preference = profile_data.language_preference  # type: ignore[assignment]
    if profile_data.timezone is not None:
        current_planner.timezone = profile_data.timezone  # type: ignore[assignment]

    current_planner.updated_at = datetime.utcnow()  # type: ignore[assignment]
    db.commit()
    db.refresh(current_planner)

    return {
        "planner_id": str(current_planner.planner_id),
        "email": current_planner.email,
        "phone": current_planner.phone,
        "full_name": current_planner.full_name,
        "company_name": current_planner.company_name,
        "whatsapp_number": current_planner.whatsapp_number,
        "language_preference": current_planner.language_preference,
        "timezone": current_planner.timezone,
        "updated_at": current_planner.updated_at,
    }
