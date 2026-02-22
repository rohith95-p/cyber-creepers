import sys
import os

# Add the project root (rohith) directory to the sys.path so modules like 'src' and 'app' resolve correctly in tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
