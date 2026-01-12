"""
Rate limiting functionality
"""
import time
from typing import List
from config.settings import RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW

class RateLimiter:
    """Simple rate limiter for user requests"""
    
    def __init__(self):
        self.request_times: List[float] = []
        self.total_requests: int = 0
    
    def check_limit(self) -> bool:
        """Check if user has exceeded rate limit"""
        current_time = time.time()
        
        # Remove old requests outside the time window
        self.request_times = [
            t for t in self.request_times 
            if current_time - t < RATE_LIMIT_WINDOW
        ]
        
        if len(self.request_times) >= RATE_LIMIT_REQUESTS:
            return False
        
        self.request_times.append(current_time)
        self.total_requests += 1
        return True
    
    def get_remaining(self) -> int:
        """Get remaining requests in current window"""
        return max(0, RATE_LIMIT_REQUESTS - len(self.request_times))
    
    def get_total(self) -> int:
        """Get total requests made"""
        return self.total_requests