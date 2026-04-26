"""
Authentication Routes
Handles planner registration, login, and token management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_planner
from app.models.planner import Planner
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
                        "expires_in": 1800
                    }
                }
            }
        },
        400: {"description": "Invalid input or email already exists"},
        422: {"description": "Validation error"}
    }
)
async def register_planner(
    planner_data: PlannerRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new planner account.
    
    - **email**: Valid email address (must be unique)
    - **password**: Minimum 8 characters
    - **full_name**: Planner's full name
    - **phone_number**: Phone number with country code
    - **business_name**: Optional business/company name
    """
    # TODO: Implement registration logic
    return {"message": "Registration endpoint - to be implemented"}


@router.post(
    "/login",
    response_model=Token,
    summary="Login",
    description="Authenticate planner and receive access tokens",
    responses={
        200: {"description": "Successfully authenticated"},
        401: {"description": "Invalid credentials"},
        422: {"description": "Validation error"}
    }
)
async def login(
    credentials: PlannerLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password.
    
    Returns JWT access token and refresh token for authenticated requests.
    
    - **email**: Registered email address
    - **password**: Account password
    """
    # TODO: Implement login logic
    return {"message": "Login endpoint - to be implemented"}


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh Access Token",
    description="Get a new access token using a valid refresh token",
    responses={
        200: {"description": "Token successfully refreshed"},
        401: {"description": "Invalid or expired refresh token"}
    }
)
async def refresh_token(token_data: TokenRefresh):
    """
    Refresh access token using refresh token.
    
    Use this endpoint when the access token expires to get a new one
    without requiring the user to login again.
    
    - **refresh_token**: Valid refresh token from login/register
    """
    # TODO: Implement token refresh logic
    return {"message": "Token refresh endpoint - to be implemented"}


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout",
    description="Logout current planner and invalidate tokens",
    responses={
        200: {"description": "Successfully logged out"},
        401: {"description": "Not authenticated"}
    }
)
async def logout(current_planner: Planner = Depends(get_current_planner)):
    """
    Logout current planner.
    
    Invalidates the current access and refresh tokens.
    Requires authentication.
    """
    # TODO: Implement logout logic
    return {"message": "Logout endpoint - to be implemented"}


@router.post(
    "/verify-email",
    response_model=MessageResponse,
    summary="Verify Email",
    description="Verify planner's email address using verification token",
    responses={
        200: {"description": "Email successfully verified"},
        400: {"description": "Invalid or expired token"}
    }
)
async def verify_email(verification: EmailVerification):
    """
    Verify planner email address.
    
    Use the verification token sent to the email address during registration.
    
    - **token**: Email verification token
    """
    # TODO: Implement email verification logic
    return {"message": "Email verification endpoint - to be implemented"}


@router.post(
    "/forgot-password",
    response_model=MessageResponse,
    summary="Request Password Reset",
    description="Request a password reset link to be sent to email",
    responses={
        200: {"description": "Password reset email sent"},
        404: {"description": "Email not found"}
    }
)
async def forgot_password(reset_request: PasswordReset):
    """
    Request password reset.
    
    Sends a password reset link to the provided email address if it exists.
    
    - **email**: Registered email address
    """
    # TODO: Implement password reset request logic
    return {"message": "Forgot password endpoint - to be implemented"}


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    summary="Reset Password",
    description="Reset password using the token from reset email",
    responses={
        200: {"description": "Password successfully reset"},
        400: {"description": "Invalid or expired token"}
    }
)
async def reset_password(reset_data: PasswordResetConfirm):
    """
    Reset password with token.
    
    Use the token received in the password reset email to set a new password.
    
    - **token**: Password reset token from email
    - **new_password**: New password (minimum 8 characters)
    """
    # TODO: Implement password reset logic
    return {"message": "Reset password endpoint - to be implemented"}


@router.get(
    "/me",
    response_model=PlannerResponse,
    summary="Get Current Planner",
    description="Get the currently authenticated planner's profile information",
    responses={
        200: {"description": "Planner profile retrieved"},
        401: {"description": "Not authenticated"}
    }
)
async def get_current_planner_profile(
    current_planner: Planner = Depends(get_current_planner)
):
    """
    Get current planner profile.
    
    Returns the profile information of the currently authenticated planner.
    Requires authentication.
    """
    # TODO: Implement get current planner logic
    return {"message": "Get current planner endpoint - to be implemented"}

# Made with Bob
