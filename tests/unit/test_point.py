import pytest
from fullcontrol.point import Point

def test_point_initialization():
    # Test default initialization
    p1 = Point()
    assert p1.x is None
    assert p1.y is None
    assert p1.z is None
    
    # Test initialization with values
    p2 = Point(x=1.0, y=2.0, z=3.0)
    assert p2.x == 1.0
    assert p2.y == 2.0
    assert p2.z == 3.0
    
    # Test initialization with partial values
    p3 = Point(x=1.0, y=2.0)
    assert p3.x == 1.0
    assert p3.y == 2.0
    assert p3.z is None

def test_point_equality():
    p1 = Point(x=1.0, y=2.0, z=3.0)
    p2 = Point(x=1.0, y=2.0, z=3.0)
    p3 = Point(x=1.0, y=2.0, z=4.0)
    
    assert p1 == p2
    assert p1 != p3

def test_point_creation():
    """Test creating points with different coordinate combinations"""
    # Test with all coordinates
    p1 = Point(x=1.0, y=2.0, z=3.0)
    assert p1.x == 1.0
    assert p1.y == 2.0
    assert p1.z == 3.0

    # Test with partial coordinates
    p2 = Point(x=1.0, y=2.0)
    assert p2.x == 1.0
    assert p2.y == 2.0
    assert p2.z is None

    # Test empty point
    p3 = Point()
    assert p3.x is None
    assert p3.y is None
    assert p3.z is None

def test_point_dict_access():
    """Test dictionary-style access inherited from BaseModelPlus"""
    point = Point(x=1.0, y=2.0, z=3.0)
    assert point["x"] == 1.0
    assert point["y"] == 2.0
    assert point["z"] == 3.0

def test_point_update():
    """Test updating point coordinates"""
    point = Point(x=1.0, y=2.0)
    point["z"] = 3.0
    assert point.z == 3.0

def test_point_update_from():
    """Test updating from another point"""
    p1 = Point(x=1.0, y=2.0)
    p2 = Point(y=3.0, z=4.0)
    p1.update_from(p2)
    assert p1.x == 1.0  # Should keep original value
    assert p1.y == 3.0  # Should update
    assert p1.z == 4.0  # Should update