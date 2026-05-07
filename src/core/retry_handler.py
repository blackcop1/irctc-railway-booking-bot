"""Smart retry logic with exponential backoff"""

import time
import asyncio
from typing import Callable, Any, Optional, TypeVar
from ..utils.logger import setup_logger
from ..utils.constants import MAX_RETRIES, INITIAL_RETRY_DELAY, MAX_RETRY_DELAY, BACKOFF_MULTIPLIER

logger = setup_logger(__name__)

T = TypeVar('T')


class RetryHandler:
    """Handle retries with exponential backoff"""

    def __init__(
        self,
        max_attempts: int = MAX_RETRIES,
        initial_delay: float = INITIAL_RETRY_DELAY,
        max_delay: float = MAX_RETRY_DELAY,
        backoff_multiplier: float = BACKOFF_MULTIPLIER
    ):
        """Initialize retry handler
        
        Args:
            max_attempts: Maximum number of retry attempts
            initial_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            backoff_multiplier: Multiplier for exponential backoff
        """
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_multiplier = backoff_multiplier
    
    def execute(
        self,
        func: Callable[..., T],
        *args: Any,
        on_retry: Optional[Callable] = None,
        **kwargs: Any
    ) -> T:
        """Execute function with retry logic
        
        Args:
            func: Function to execute
            *args: Positional arguments for function
            on_retry: Callback function on retry
            **kwargs: Keyword arguments for function
        
        Returns:
            Function result
        
        Raises:
            Exception: If all retries exhausted
        """
        attempt = 0
        delay = self.initial_delay
        
        while attempt < self.max_attempts:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                attempt += 1
                
                if attempt >= self.max_attempts:
                    logger.error(f"All {self.max_attempts} retry attempts failed")
                    raise
                
                logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                
                if on_retry:
                    on_retry(attempt, delay, e)
                
                time.sleep(delay)
                delay = min(delay * self.backoff_multiplier, self.max_delay)
        
        raise RuntimeError(f"Failed after {self.max_attempts} attempts")
    
    def get_retry_schedule(self) -> list:
        """Get calculated retry delay schedule
        
        Returns:
            List of delay times for each retry
        """
        schedule = []
        delay = self.initial_delay
        
        for _ in range(self.max_attempts):
            schedule.append(delay)
            delay = min(delay * self.backoff_multiplier, self.max_delay)
        
        return schedule
