import pytest
from fullcontrol.geometry.vector import Vector

def test_vector_initialization():
    # Test empty initialization
    v = Vector()
    assert v.x is None
    assert v.y is None
    assert v.z is None
    
    # Test full initialization
    v = Vector(x=1.0, y=2.0, z=3.0)
    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z == 3.0
    
    # Test partial initialization
    v = Vector(x=1.0, y=2.0)
    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z is None

def test_vector_updates():
    v = Vector()
    
    # Test setting values
    v.x = 1.0
    v.y = 2.0
    v.z = 3.0
    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z == 3.0
    
    # Test updating values
    v.x = 4.0
    assert v.x == 4.0

def test_vector_validation():
    # Test invalid x value
    with pytest.raises(Exception):
        Vector(x="not a number", y=1.0, z=1.0)
    
    # Test invalid y value
    with pytest.raises(Exception):
        Vector(x=1.0, y="not a number", z=1.0)
    
    # Test invalid z value
    with pytest.raises(Exception):
        Vector(x=1.0, y=1.0, z="not a number")