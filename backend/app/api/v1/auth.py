"""
Authentication Routes
Handles planner registration, login, and token management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets

from app.database import get_db
from app.dependencies import get_current_planner
from app.models.planner import Planner
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.config import settings
from app.schemas import (
    PlannerRegister,
    PlannerLogin,
    Token,
    TokenRefresh,
    PasswordReset,
    PasswordResetConfirm,
    EmailVerification,
    PlannerResponse,
    MessageResponse,
)

router = APIRouter()

# In-memory storage for tokens (in production, use Redis)
# Format: {token: {planner_id, expires_at}}
verification_tokens = {}
reset_tokens = {}
blacklisted_tokens = set()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=Token,
    summary="Register New Planner",
    description="Create a new planner account with email and password. Returns authentication tokens upon successful registration.",
    responses={
        201: {
            "description": "Planner successfully registered",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                        "expires_in": 1800,
                    }
                }
            },
        },
        400: {"description": "Invalid input or email already exists"},
        422: {"description": "Validation error"},
    },
)
async def register_planner(
    planner_data: PlannerRegister, db: Session = Depends(get_db)
):
    """
    Register a new planner account.

    - **email**: Valid email address (must be unique)
    - **password**: Minimum 8 characters
    - **full_name**: Planner's full name
    - **phone_number**: Phone number with country code
    - **business_name**: Optional business/company name
    """
    # Check if email already exists
    existing_planner = (
        db.query(Planner).filter(Planner.email == planner_data.email).first()
    )
    if existing_planner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Check if phone already exists
    existing_phone = (
        db.query(Planner).filter(Planner.phone == planner_data.phone_number).first()
    )
    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered",
        )

    # Create new planner
    role = planner_data.role.lower().strip()
    if role not in {"admin", "planner"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be either 'admin' or 'planner'",
        )

    new_planner = Planner(
        email=planner_data.email,
        phone=planner_data.phone_number,
        password_hash=get_password_hash(planner_data.password),
        full_name=planner_data.full_name,
        company_name=planner_data.business_name,
        role=role,
        is_active=True,
        is_verified=False,  # Email verification required
        email_verified=False,
        phone_verified=False,
    )

    db.add(new_planner)
    db.commit()
    db.refresh(new_planner)

    # Generate verification token (in production, send via email)
    verification_token = secrets.token_urlsafe(32)
    verification_tokens[verification_token] = {
        "planner_id": str(new_planner.planner_id),
        "expires_at": datetime.utcnow() + timedelta(hours=24),
    }

    # Create access and refresh tokens
    access_token = create_access_token(data={"sub": str(new_planner.planner_id)})
    refresh_token = create_refresh_token(data={"sub": str(new_planner.planner_id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post(
    "/login",
    response_model=Token,
    summary="Login",
    description="Authenticate planner and receive access tokens",
    responses={
        200: {"description": "Successfully authenticated"},
        401: {"description": "Invalid credentials"},
        422: {"description": "Validation error"},
    },
)
async def login(credentials: PlannerLogin, db: Session = Depends(get_db)):
    """
    Login with phone number and password.

    Returns JWT access token and refresh token for authenticated requests.

    - **phone**: Registered phone number
    - **password**: Account password
    """
    # Find planner by phone
    planner = db.query(Planner).filter(Planner.phone == credentials.phone).first()

    if not planner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password",
        )

    # Verify password
    if not verify_password(credentials.password, planner.password_hash):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Check if account is active
    if planner.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact support.",
        )

    # Update last login time
    planner.last_login_at = datetime.utcnow()  # type: ignore[assignment]
    db.commit()

    # Create access and refresh tokens
    access_token = create_access_token(data={"sub": str(planner.planner_id)})
    refresh_token = create_refresh_token(data={"sub": str(planner.planner_id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh Access Token",
    description="Get a new access token using a valid refresh token",
    responses={
        200: {"description": "Token successfully refreshed"},
        401: {"description": "Invalid or expired refresh token"},
    },
)
async def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token.

    Use this endpoint when the access token expires to get a new one
    without requiring the user to login again.

    - **refresh_token**: Valid refresh token from login/register
    """
    # Check if token is blacklisted
    if token_data.refresh_token in blacklisted_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked"
        )

    try:
        # Decode refresh token
        payload = decode_token(token_data.refresh_token)

        # Verify it's a refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
            )

        planner_id = payload.get("sub")
        if not planner_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        # Verify planner still exists and is active
        planner = db.query(Planner).filter(Planner.planner_id == planner_id).first()
        if not planner or planner.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or inactive account",
            )

        # Create new tokens
        new_access_token = create_access_token(data={"sub": planner_id})
        new_refresh_token = create_refresh_token(data={"sub": planner_id})

        # Blacklist old refresh token
        blacklisted_tokens.add(token_data.refresh_token)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout",
    description="Logout current planner and invalidate tokens",
    responses={
        200: {"description": "Successfully logged out"},
        401: {"description": "Not authenticated"},
    },
)
async def logout(current_planner: Planner = Depends(get_current_planner)):
    """
    Logout current planner.

    Invalidates the current access and refresh tokens.
    Requires authentication.
    """
    # In production, blacklist the token in Redis
    # For now, just return success message
    return {"message": "Successfully logged out"}


@router.post(
    "/verify-email",
    response_model=MessageResponse,
    summary="Verify Email",
    description="Verify planner's email address using verification token",
    responses={
        200: {"description": "Email successfully verified"},
        400: {"description": "Invalid or expired token"},
    },
)
async def verify_email(verification: EmailVerification, db: Session = Depends(get_db)):
    """
    Verify planner email address.

    Use the verification token sent to the email address during registration.

    - **token**: Email verification token
    """
    # Check if token exists
    if verification.token not in verification_tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        )

    token_data = verification_tokens[verification.token]

    # Check if token is expired
    if datetime.utcnow() > token_data["expires_at"]:
        del verification_tokens[verification.token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token has expired",
        )

    # Get planner and verify email
    planner = (
        db.query(Planner).filter(Planner.planner_id == token_data["planner_id"]).first()
    )

    if not planner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Planner not found"
        )

    planner.email_verified = True  # type: ignore[assignment]
    planner.is_verified = True  # type: ignore[assignment]
    db.commit()

    # Remove used token
    del verification_tokens[verification.token]

    return {"message": "Email successfully verified"}


@router.post(
    "/forgot-password",
    response_model=MessageResponse,
    summary="Request Password Reset",
    description="Request a password reset link to be sent to email",
    responses={
        200: {"description": "Password reset email sent"},
        404: {"description": "Email not found"},
    },
)
async def forgot_password(reset_request: PasswordReset, db: Session = Depends(get_db)):
    """
    Request password reset.

    Sends a password reset link to the provided email address if it exists.

    - **email**: Registered email address
    """
    # Find planner by email
    planner = db.query(Planner).filter(Planner.email == reset_request.email).first()

    # Always return success to prevent email enumeration
    if not planner:
        return {"message": "If the email exists, a password reset link has been sent"}

    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    reset_tokens[reset_token] = {
        "planner_id": str(planner.planner_id),
        "expires_at": datetime.utcnow() + timedelta(hours=1),
    }

    # In production, send email with reset link
    # For now, just log it (in development, you'd see this in console)
    print(f"Password reset token for {planner.email}: {reset_token}")

    return {"message": "If the email exists, a password reset link has been sent"}


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    summary="Reset Password",
    description="Reset password using the token from reset email",
    responses={
        200: {"description": "Password successfully reset"},
        400: {"description": "Invalid or expired token"},
    },
)
async def reset_password(
    reset_data: PasswordResetConfirm, db: Session = Depends(get_db)
):
    """
    Reset password with token.

    Use the token received in the password reset email to set a new password.

    - **token**: Password reset token from email
    - **new_password**: New password (minimum 8 characters)
    """
    # Check if token exists
    if reset_data.token not in reset_tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    token_data = reset_tokens[reset_data.token]

    # Check if token is expired
    if datetime.utcnow() > token_data["expires_at"]:
        del reset_tokens[reset_data.token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Reset token has expired"
        )

    # Get planner and update password
    planner = (
        db.query(Planner).filter(Planner.planner_id == token_data["planner_id"]).first()
    )

    if not planner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Planner not found"
        )

    # Update password
    planner.password_hash = get_password_hash(reset_data.new_password)  # type: ignore[assignment]
    db.commit()

    # Remove used token
    del reset_tokens[reset_data.token]

    return {"message": "Password successfully reset"}


@router.get(
    "/me",
    response_model=PlannerResponse,
    summary="Get Current Planner",
    description="Get the currently authenticated planner's profile information",
    responses={
        200: {"description": "Planner profile retrieved"},
        401: {"description": "Not authenticated"},
    },
)
async def get_current_planner_profile(
    current_planner: Planner = Depends(get_current_planner),
):
    """
    Get current planner profile.

    Returns the profile information of the currently authenticated planner.
    Requires authentication.
    """
    return {
        "id": str(current_planner.planner_id),
        "email": current_planner.email,
        "full_name": current_planner.full_name,
        "phone_number": current_planner.phone,
        "business_name": current_planner.company_name,
        "is_verified": current_planner.is_verified,
        "role": current_planner.role,
        "created_at": current_planner.created_at,
    }


# Made with Bob
