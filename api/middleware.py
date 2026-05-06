
from collections import defaultdict, deque
from time import time
from fastapi import Request

from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    
    def __init__(self, app, requests_per_minute: int = 10):
        super().__init__(app,)
        self.limit = requests_per_minute
        self.window = 60

        self.requests = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):

        client_ip = request.client.host if request.client else "unknown"

        now = time.time()

        history = self.requests[client_ip]

        while history and history[0] < now - self.window:
            history.popleft()

        if len(history) >= self.limit:
            return JSONResponse(
                status_code=429,
                content={"error": "Too many requests",
                         "details": f"Rate limit of {self.limit} requests per minute exceeded."
                        }
            )
        
        history.append(now)

        response = await call_next(request)
        return response