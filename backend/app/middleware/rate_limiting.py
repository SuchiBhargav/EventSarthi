"""
Rate Limiting Middleware
Prevents API abuse by limiting request rates per client
"""

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce rate limiting

    Uses in-memory storage for rate limit tracking.
    In production, use Redis for distributed rate limiting.
    """

    def __init__(self, app, requests_per_minute: int = 60):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per client
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Store: {client_id: (request_count, window_start_time)}
        self.request_counts: Dict[str, Tuple[int, datetime]] = defaultdict(
            lambda: (0, datetime.utcnow())
        )
        self.window_duration = timedelta(minutes=1)

    def get_client_id(self, request: Request) -> str:
        """
        Get unique client identifier

        Uses planner_id if authenticated, otherwise uses IP address
        """
        # Try to get planner_id from request state (set by tenant isolation middleware)
        planner_id = getattr(request.state, "planner_id", None)
        if planner_id:
            return f"planner:{planner_id}"

        # Fall back to IP address for unauthenticated requests
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"

    def is_rate_limited(self, client_id: str) -> bool:
        """
        Check if client has exceeded rate limit

        Args:
            client_id: Unique client identifier

        Returns:
            bool: True if rate limited, False otherwise
        """
        current_time = datetime.utcnow()
        count, window_start = self.request_counts[client_id]

        # Check if we're still in the same time window
        if current_time - window_start < self.window_duration:
            # Same window - check if limit exceeded
            if count >= self.requests_per_minute:
                return True
            # Increment count
            self.request_counts[client_id] = (count + 1, window_start)
        else:
            # New window - reset count
            self.request_counts[client_id] = (1, current_time)

        return False

    def cleanup_old_entries(self):
        """
        Remove expired entries from memory

        Called periodically to prevent memory leaks
        """
        current_time = datetime.utcnow()
        expired_keys = [
            key
            for key, (_, window_start) in self.request_counts.items()
            if current_time - window_start > self.window_duration * 2
        ]
        for key in expired_keys:
            del self.request_counts[key]

    async def dispatch(self, request: Request, call_next):
        """
        Process request and enforce rate limiting
        """
        # Skip rate limiting for health check endpoints
        if request.url.path in ["/health", "/", "/docs", "/openapi.json"]:
            return await call_next(request)

        # Get client identifier
        client_id = self.get_client_id(request)

        # Check rate limit
        if self.is_rate_limited(client_id):
            logger.warning(f"Rate limit exceeded for client: {client_id}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later.",
                headers={"Retry-After": "60"},
            )

        # Cleanup old entries occasionally (every 100th request)
        if len(self.request_counts) % 100 == 0:
            self.cleanup_old_entries()

        # Process request
        response = await call_next(request)

        # Add rate limit headers to response
        count, window_start = self.request_counts[client_id]
        remaining = max(0, self.requests_per_minute - count)
        reset_time = int((window_start + self.window_duration).timestamp())

        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset_time)

        return response


# Made with Bob
