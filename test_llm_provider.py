#!/usr/bin/env python3
"""
Test the LLM provider configuration
"""

import os
import sys
from pathlib import Path

# Add the rohith/src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "rohith" / "src"))

from dotenv import load_dotenv
from utils.llm_provider import get_llm

load_dotenv()

def test_llm():
    print("=" * 70)
    print(" Testing LLM Provider ".center(70))
    print("=" * 70)
    
    provider = os.getenv("LLM_PROVIDER", "google").lower()
    print(f"\n📋 Provider: {provider.upper()}")
    
    # Check API keys
    if provider == "groq":
        key = os.getenv("GROQ_API_KEY")
        print(f"✓ GROQ_API_KEY: {'Set' if key else '❌ NOT SET'}")
        if not key:
            print("  → Get it from: https://console.groq.com")
            return False
    
    elif provider == "openrouter":
        key = os.getenv("OPENROUTER_API_KEY")
        print(f"✓ OPENROUTER_API_KEY: {'Set' if key else '❌ NOT SET'}")
        if not key:
            print("  → Get it from: https://openrouter.ai")
            return False
    
    elif provider == "google":
        key = os.getenv("GOOGLE_API_KEY")
        print(f"✓ GOOGLE_API_KEY: {'Set' if key else '❌ NOT SET'}")
        if not key:
            print("  → Get it from: https://console.cloud.google.com")
            return False
    
    elif provider == "ollama":
        print("✓ Using local Ollama (no API key needed)")
        print("  → Make sure Ollama is running: https://ollama.ai")
    
    # Test the LLM
    print("\n🧪 Testing LLM initialization...")
    try:
        llm = get_llm(temperature=0.3)
        print("✓ LLM initialized successfully!\n")
    except Exception as e:
        print(f"❌ Error initializing LLM: {e}\n")
        return False
    
    # Test a simple inference
    print("📝 Testing inference...")
    print("   Prompt: 'Say hello in one word!'\n")
    
    try:
        response = llm.invoke("Say hello in one word!")
        print(f"✓ Response: {response.content}\n")
        print("=" * 70)
        print(" ✅ All tests passed! Your LLM provider is ready to use.".center(70))
        print("=" * 70)
        return True
    
    except Exception as e:
        print(f"❌ Error during inference: {e}\n")
        
        if provider == "groq":
            print("   Troubleshooting:")
            print("   - Check your GROQ_API_KEY is correct")
            print("   - Make sure it's not expired")
            print("   - Try creating a new key at https://console.groq.com")
        
        elif provider == "ollama":
            print("   Troubleshooting:")
            print("   - Is Ollama running? Check: http://localhost:11434")
            print("   - Install a model: ollama pull llama-2")
            print("   - Or download from: https://ollama.ai")
        
        return False

if __name__ == "__main__":
    success = test_llm()
    sys.exit(0 if success else 1)
