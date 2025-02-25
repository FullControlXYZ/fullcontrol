import pytest
import os
import sys

# Add the project root directory to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define fixtures that can be reused across multiple test files
@pytest.fixture
def sample_fixture():
    """Example fixture that can be used in tests."""
    # Setup code
    data = {'key': 'value'}
    yield data
    # Teardown code (if needed)
