import pytest
from streamlit.testing.v1 import AppTest
import os

def test_streamlit_ui_flow():
    # Initialize the Streamlit app test environment
    app_path = os.path.join(os.path.dirname(__file__), '..', 'app.py')
    at = AppTest.from_file(app_path)
    
    # Avoid making actual API calls during UI rendering test
    os.environ['GOOGLE_API_KEY'] = 'mock_key_for_testing'
    
    # Run the initial render
    at.run(timeout=10)
    
    # Verify the app loaded correctly without exceptions
    assert not at.exception, f"App crashed on load: {at.exception}"
    
    # Check if the main title is rendered (app uses "Wealth Advisory Terminal" / "Ivy Wealth AI")
    titles_text = " ".join(t.value for t in at.title) if at.title else ""
    assert "Wealth Advisory Terminal" in titles_text or "Ivy Wealth AI" in titles_text, "Main title not found."
