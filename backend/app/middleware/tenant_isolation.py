"""
Tenant Isolation Middleware
Ensures complete data isolation between planners
"""

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging
import jwt
from jwt.exceptions import InvalidTokenError

from app.config import settings

logger = logging.getLogger(__name__)


class TenantIsolationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce tenant isolation
    Adds planner_id context to requests for audit logging
    """

    async def dispatch(self, request: Request, call_next):
        """
        Process request and add tenant context

        Extracts planner_id from JWT token and adds it to request state
        for logging and audit purposes. The actual tenant isolation is
        enforced at the database query level in dependencies.py
        """
        planner_id = None

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            try:
                # Decode token to get planner_id
                payload = jwt.decode(
                    token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
                )
                planner_id = payload.get("sub")
            except InvalidTokenError:
                # Token is invalid, but we don't raise error here
                # Let the endpoint dependencies handle authentication
                pass

        # Add planner_id to request state for logging
        request.state.planner_id = planner_id

        # Log request with tenant context
        if planner_id:
            logger.info(
                f"Request from planner {planner_id}: {request.method} {request.url.path}"
            )

        response = await call_next(request)

        # Add tenant context to response headers for debugging (optional)
        if planner_id and settings.DEBUG:
            response.headers["X-Tenant-ID"] = str(planner_id)

        return response


# Made with Bob
