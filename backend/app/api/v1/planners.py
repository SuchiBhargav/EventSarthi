"""
Planner Management Routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_planner
from app.models.planner import Planner

router = APIRouter()

@router.get("/me")
async def get_current_planner_profile(
    current_planner: Planner = Depends(get_current_planner)
):
    """Get current planner profile"""
    return {"message": "Get planner profile - to be implemented"}

@router.put("/me")
async def update_planner_profile(
    current_planner: Planner = Depends(get_current_planner),
    db: Session = Depends(get_db)
):
    """Update planner profile"""
    return {"message": "Update planner profile - to be implemented"}
