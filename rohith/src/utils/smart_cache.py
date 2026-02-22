import os
import hashlib
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

CACHE_DIR = Path("./agent_cache")
CACHE_DIR.mkdir(exist_ok=True)

def get_cached_or_compute(key_prefix: str, identifier: str, data: dict, compute_fn, ttl_hours: int = 12):
    """
    Smart cache wrapper to save LLM responses to disk.
    Model-agnostic: works with OpenRouter, Google, or any backend behind compute_fn.
    If the exact same payload was requested within `ttl_hours`, returns cached result (0 API calls).
    """
    # Create deterministic hash based on node name, client, and current data payload
    cache_key = hashlib.sha256(
        f"{key_prefix}:{identifier}:{json.dumps(data, sort_keys=True)}".encode()
    ).hexdigest()
    
    cache_file = CACHE_DIR / f"{cache_key}.json"
    
    # 1. Check Cache
    if cache_file.exists():
        try:
            with open(cache_file) as f:
                cached = json.load(f)
                cached_time = datetime.fromisoformat(cached["timestamp"])
                if datetime.now() - cached_time < timedelta(hours=ttl_hours):
                    logger.info(f"CACHE HIT [{key_prefix}] -> Saved 1 API Request!")
                    return cached["result"]
        except Exception as e:
            logger.warning(f"Failed to read cache {cache_file}: {e}")
            
    # 2. Compute Fresh (Cache Miss)
    logger.info(f"CACHE MISS [{key_prefix}] -> Making Live API Call...")
    result = compute_fn()
    
    # 3. Save to disk
    try:
        with open(cache_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "result": result
            }, f)
    except Exception as e:
        logger.warning(f"Failed to write cache {cache_file}: {e}")
        
    return result
