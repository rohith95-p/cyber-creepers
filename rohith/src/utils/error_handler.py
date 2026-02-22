import time
import logging
import threading
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

# Global lock to serialize LLM calls and avoid strict concurrent rate limits (HTTP 429)
llm_lock = threading.Lock()

class IvyError(Exception):
    """Base exception for Ivy ecosystem."""
    pass

class MarketDataError(IvyError):
    pass

class LLMRateLimitError(IvyError):
    pass

class DatabaseConnectionError(IvyError):
    pass

def handle_rate_limit(retry_state):
    logger.warning(f"Rate limited. Retrying... Attempt {retry_state.attempt_number}")

# Retry decorator for LLM calls
llm_retry = retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=5, max=60),
    retry=retry_if_exception_type(Exception),
    after=handle_rate_limit
)

@llm_retry
def safe_llm_invoke(llm, prompt):
    """
    Globally synchronized LLM call to avoid rate limits (15 RPM on free tiers, etc.).
    Model-agnostic: works with OpenRouter, Google, OpenAI, or any LangChain LLM.
    Uses a 3.5s stagger to throttle parallel LangGraph nodes.
    """
    with llm_lock:
        time.sleep(3.5)
        return llm.invoke(prompt)

def graceful_fallback(fallback_value):
    """Decorator to return a fallback value upon failure."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}. Using fallback.")
                return fallback_value
        return wrapper
    return decorator
