"""
Authentication Schemas
Pydantic models for authentication requests and responses
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class PlannerRegister(BaseModel):
    """Schema for planner registration"""

    email: EmailStr = Field(
        ..., description="Planner's email address", json_schema_extra={"example": "planner@example.com"}
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password (minimum 8 characters)",
        json_schema_extra={"example": "SecurePass123!"},
    )
    full_name: str = Field(
        ..., min_length=2, max_length=100, description="Full name", json_schema_extra={"example": "John Doe"}
    )
    phone_number: str = Field(
        ..., description="Phone number with country code", json_schema_extra={"example": "+1234567890"}
    )
    business_name: Optional[str] = Field(
        None, description="Business or company name", json_schema_extra={"example": "Elite Events"}
    )
    role: str = Field(
        default="planner",
        description="User role: admin for internal team, planner for event planners",
        json_schema_extra={"example": "planner"},
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "planner@example.com",
                "password": "SecurePass123!",
                "full_name": "John Doe",
                "phone_number": "+1234567890",
                "business_name": "Elite Events",
                "role": "planner",
            }
        }


class PlannerLogin(BaseModel):
    """Schema for planner login"""

    phone: str = Field(
        ..., description="Planner's phone number", json_schema_extra={"example": "+1234567890"}
    )
    password: str = Field(
        ..., description="Password", json_schema_extra={"example": "SecurePass123!"}
    )

    class Config:
        json_schema_extra = {
            "example": {"phone": "+1234567890", "password": "SecurePass123!"}
        }


class Token(BaseModel):
    """Schema for authentication token response"""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
            }
        }


class TokenRefresh(BaseModel):
    """Schema for token refresh request"""

    refresh_token: str = Field(..., description="Refresh token")

    class Config:
        json_schema_extra = {
            "example": {"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
        }


class PasswordReset(BaseModel):
    """Schema for password reset request"""

    email: EmailStr = Field(..., description="Email address for password reset")

    class Config:
        json_schema_extra = {"example": {"email": "planner@example.com"}}


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation"""

    token: str = Field(..., description="Password reset token")
    new_password: str = Field(
        ..., min_length=8, description="New password (minimum 8 characters)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "token": "reset-token-here",
                "new_password": "NewSecurePass123!",
            }
        }


class EmailVerification(BaseModel):
    """Schema for email verification"""

    token: str = Field(..., description="Email verification token")

    class Config:
        json_schema_extra = {"example": {"token": "verification-token-here"}}


class PlannerResponse(BaseModel):
    """Schema for planner information response"""

    id: str = Field(..., description="Planner unique identifier")
    email: EmailStr = Field(..., description="Planner's email address")
    full_name: str = Field(..., description="Full name")
    phone_number: str = Field(..., description="Phone number")
    business_name: Optional[str] = Field(None, description="Business name")
    is_verified: bool = Field(..., description="Email verification status")
    role: str = Field(..., description="Role of the authenticated user")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "planner_123abc",
                "email": "planner@example.com",
                "full_name": "John Doe",
                "phone_number": "+1234567890",
                "business_name": "Elite Events",
                "is_verified": True,
                "role": "planner",
                "created_at": "2024-01-15T10:30:00Z",
            }
        }


class MessageResponse(BaseModel):
    """Generic message response"""

    message: str = Field(..., description="Response message")

    class Config:
        json_schema_extra = {"example": {"message": "Operation completed successfully"}}


# Made with Bob
