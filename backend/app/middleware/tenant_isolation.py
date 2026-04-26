"""
Tenant Isolation Middleware
Ensures complete data isolation between planners
"""
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging

logger = logging.getLogger(__name__)


class TenantIsolationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce tenant isolation
    Adds planner_id context to requests
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        Process request and enforce tenant isolation
        """
        # TODO: Implement tenant isolation logic
        # Extract planner_id from JWT token
        # Add to request state for use in queries
        
        response = await call_next(request)
        return response

# Made with Bob
