"""
Dependency Injection Functions
Common dependencies used across the application
"""
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import datetime

from app.database import get_db
from app.config import settings
from app.models.planner import Planner
from app.models.event import Event

# Security scheme for JWT
security = HTTPBearer()


def get_current_planner(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Planner:
    """
    Get current authenticated planner from JWT token
    
    Args:
        credentials: JWT token from Authorization header
        db: Database session
        
    Returns:
        Planner: Authenticated planner object
        
    Raises:
        HTTPException: If token is invalid or planner not found
    """
    token = credentials.credentials
    
    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        planner_id: Optional[str] = payload.get("sub")
        
        if planner_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
            
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    # Get planner from database
    planner = db.query(Planner).filter(Planner.planner_id == planner_id).first()
    
    if planner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Planner not found"
        )
    
    if planner.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Planner account is inactive"
        )
    
    return planner


def get_current_active_planner(
    current_planner: Planner = Depends(get_current_planner)
) -> Planner:
    """
    Get current active planner (additional check)
    
    Args:
        current_planner: Current planner from get_current_planner
        
    Returns:
        Planner: Active planner object
        
    Raises:
        HTTPException: If planner is not active
    """
    if current_planner.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive planner"
        )
    return current_planner


def verify_event_access(
    event_id: str,
    current_planner: Planner = Depends(get_current_planner),
    db: Session = Depends(get_db)
) -> Event:
    """
    Verify that the current planner has access to the specified event
    
    Args:
        event_id: Event ID to verify access for
        current_planner: Current authenticated planner
        db: Database session
        
    Returns:
        Event: Event object if access is granted
        
    Raises:
        HTTPException: If event not found or access denied
    """
    event = db.query(Event).filter(
        Event.event_id == event_id,
        Event.planner_id == current_planner.planner_id
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found or access denied"
        )
    
    return event


def get_whatsapp_signature(
    x_hub_signature_256: Optional[str] = Header(None)
) -> Optional[str]:
    """
    Extract WhatsApp webhook signature from headers
    
    Args:
        x_hub_signature_256: Signature header from WhatsApp
        
    Returns:
        Optional[str]: Signature value or None
    """
    return x_hub_signature_256


def verify_whatsapp_webhook(
    hub_mode: Optional[str] = None,
    hub_verify_token: Optional[str] = None,
    hub_challenge: Optional[str] = None
) -> dict:
    """
    Verify WhatsApp webhook subscription
    
    Args:
        hub_mode: Mode from WhatsApp (should be 'subscribe')
        hub_verify_token: Verification token
        hub_challenge: Challenge string to return
        
    Returns:
        dict: Challenge response
        
    Raises:
        HTTPException: If verification fails
    """
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN:
        return {"hub.challenge": hub_challenge}
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Webhook verification failed"
    )


class PaginationParams:
    """
    Common pagination parameters
    """
    def __init__(
        self,
        page: int = 1,
        page_size: int = settings.DEFAULT_PAGE_SIZE
    ):
        self.page = max(1, page)
        self.page_size = min(page_size, settings.MAX_PAGE_SIZE)
        self.skip = (self.page - 1) * self.page_size
        self.limit = self.page_size

# Made with Bob
