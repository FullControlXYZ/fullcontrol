import pytest

# Import your module(s) to test
# from fullcontrol import some_module

def test_example():
    """A simple example test."""
    assert True

def test_with_fixture(sample_fixture):
    """Example test using a fixture."""
    assert sample_fixture['key'] == 'value'

class TestExampleClass:
    """Group related tests in a class."""
    
    def test_method_one(self):
        """Test specific functionality."""
        expected = 4
        result = 2 + 2
        assert result == expected
    
    def test_method_two(self):
        """Another test."""
        assert 'hello'.upper() == 'HELLO'
