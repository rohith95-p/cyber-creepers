import time
from functools import wraps
import json
import hashlib

class SimpleMemoryCache:
    def __init__(self, ttl=300):
        self._cache = {}
        self.ttl = ttl

    def get(self, key):
        if key in self._cache:
            entry = self._cache[key]
            if time.time() - entry['time'] < self.ttl:
                return entry['data']
            else:
                del self._cache[key]
        return None

    def set(self, key, value):
        self._cache[key] = {
            'time': time.time(),
            'data': value
        }

    def invalidate(self, key):
        if key in self._cache:
            del self._cache[key]

# Global cache instance
ivy_cache = SimpleMemoryCache(ttl=300)

def cache_result(ttl=300):
    """Decorator to cache function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a deterministic key from args and kwargs
            key_data = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True, default=str)
            key = hashlib.md5(key_data.encode('utf-8')).hexdigest()
            
            cached = ivy_cache.get(key)
            if cached is not None:
                return cached
                
            result = func(*args, **kwargs)
            ivy_cache.set(key, result)
            ivy_cache.ttl = ttl # Update TTL if needed
            return result
        return wrapper
    return decorator
