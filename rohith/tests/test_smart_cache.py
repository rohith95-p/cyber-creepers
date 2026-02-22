import pytest
import os
import json
import shutil
from pathlib import Path
from src.utils.smart_cache import get_cached_or_compute, CACHE_DIR

@pytest.fixture(autouse=True)
def setup_and_teardown_cache():
    # Setup: create a temporary test cache directory or use the existing one but clear it
    if CACHE_DIR.exists():
        shutil.rmtree(CACHE_DIR)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    yield
    # Teardown: clear the cache after test
    if CACHE_DIR.exists():
        shutil.rmtree(CACHE_DIR)

def test_smart_cache_prevents_redundant_compute():
    tracker = {"compute_calls": 0}
    
    def mock_expensive_computation():
        tracker["compute_calls"] += 1
        return {"response": "Expensive AI calculation result"}
        
    client_id = "MOCK_CLIENT_999"
    payload = {"query": "Tell me about MSFT", "ticker": "MSFT"}
    
    # First call - should result in a CACHE MISS and compute
    result1 = get_cached_or_compute("test_node", client_id, payload, mock_expensive_computation)
    assert result1["response"] == "Expensive AI calculation result"
    assert tracker["compute_calls"] == 1, "Compute function was not called on cache miss."
    
    # Second call - EXACT SAME payload, should result in a CACHE HIT and NOT compute
    result2 = get_cached_or_compute("test_node", client_id, payload, mock_expensive_computation)
    assert result2["response"] == "Expensive AI calculation result"
    assert tracker["compute_calls"] == 1, "Compute function WAS called despite identical payload! Cache failed."
    
    # Third call - DIFFERENT payload, should result in a CACHE MISS and compute
    payload["query"] = "Tell me about AAPL"
    result3 = get_cached_or_compute("test_node", client_id, payload, mock_expensive_computation)
    
    assert tracker["compute_calls"] == 2, "Compute function was omitted on new payload."
