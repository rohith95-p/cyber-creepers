"""
Universal LLM Provider - Switch between Google, Groq, OpenRouter, etc. with ONE environment variable
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv()
logger = logging.getLogger(__name__)

# Global state to keep track of current key index per provider
_KEY_INDEXES = {"openrouter": 0, "google": 0, "groq": 0}

def get_keys_for_provider(provider: str) -> list:
    """Gets a list of keys from the environment for a given provider."""
    env_var = f"{provider.upper()}_API_KEY"
    raw_val = os.getenv(env_var, "")
    # Support comma-separated keys or multiple lines
    return [k.strip() for k in raw_val.replace(",", " ").split() if k.strip()]

def rotate_key(provider: str):
    """Increments the key index for the provider."""
    keys = get_keys_for_provider(provider)
    if len(keys) > 1:
        _KEY_INDEXES[provider] = (_KEY_INDEXES[provider] + 1) % len(keys)
        logger.warning(f"🔄 Rotating to next {provider} API key (New index: {_KEY_INDEXES[provider]})")

def get_llm(temperature: float = 0.3, model_override: str = None):
    """
    Get LLM instance based on environment variable with multi-key rotation support.
    """
    provider = os.getenv("LLM_PROVIDER", "google").lower()
    keys = get_keys_for_provider(provider)
    
    # Fallback to standard env var if key list is empty
    current_idx = _KEY_INDEXES.get(provider, 0)
    if not keys:
        api_key = os.getenv(f"{provider.upper()}_API_KEY")
    else:
        # Safety bound
        current_idx = current_idx % len(keys)
        api_key = keys[current_idx]
    
    if provider == "groq":
        from langchain_groq import ChatGroq
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY not set in .env")
        model = model_override or "llama-3-70b-8192"
        return ChatGroq(api_key=api_key, model=model, temperature=temperature, max_retries=3)
    
    elif provider == "openrouter":
        if not api_key:
            raise ValueError("❌ OPENROUTER_API_KEY not set in .env")
        model = model_override or "openrouter/auto"
        return ChatOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            model=model,
            temperature=temperature,
            max_retries=3
        )
    
    elif provider == "ollama":
        model = model_override or "llama-2"
        return ChatOpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            model=model,
            temperature=temperature,
            max_retries=1
        )
    
    elif provider == "google" or provider == "gemini":
        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY not set in .env")
        model = model_override or "gemini-2.0-flash"
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=temperature,
            max_retries=3
        )
    
    else:
        raise ValueError(f"❌ Unknown provider: {provider}. Use: groq, openrouter, google, or ollama")

# Example usage for direct calling with rotation
def smart_invoke(prompt: str, temperature: float = 0.3):
    """Invoke the LLM with automatic key rotation on 429 errors."""
    provider = os.getenv("LLM_PROVIDER", "google").lower()
    keys = get_keys_for_provider(provider)
    
    max_attempts = max(len(keys), 1)
    for attempt in range(max_attempts):
        try:
            llm = get_llm(temperature=temperature)
            return llm.invoke(prompt)
        except Exception as e:
            if "429" in str(e) or "rate limit" in str(e).lower():
                rotate_key(provider)
                if attempt < max_attempts - 1:
                    continue
            raise e

if __name__ == "__main__":
    print("Testing Universal LLM Provider with Rotation Logic...")
    try:
        llm = get_llm()
        print("✓ LLM initialized!")
    except Exception as e:
        print(f"Error: {e}")
