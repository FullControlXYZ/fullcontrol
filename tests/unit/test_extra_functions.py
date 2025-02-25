import pytest
from fullcontrol.extra_functions import points_only, relative_point, flatten, linspace, first_point, last_point
from fullcontrol.point import Point

def test_points_only():
    # Create test data
    p1 = Point(x=1, y=1, z=1)
    p2 = Point(x=2, y=None, z=2)
    p3 = Point(x=3, y=3, z=None)
    steps = [p1, "not a point", p2, p3]
    
    # Test without tracking
    result = points_only(steps, track_xyz=False)
    assert len(result) == 3
    assert all(isinstance(p, Point) for p in result)
    assert result[1].y is None
    assert result[2].z is None
    
    # Test with tracking
    result = points_only(steps, track_xyz=True)
    assert len(result) == 2  # First fully defined point and after
    assert all(isinstance(p, Point) for p in result)
    assert result[0].x == 1 and result[0].y == 1 and result[0].z == 1
    assert result[1].y == 1  # Should inherit y from previous point

def test_relative_point():
    # Test with single point
    ref_point = Point(x=1, y=1, z=1)
    rel_point = relative_point(ref_point, 2, 3, 4)
    assert rel_point.x == 3
    assert rel_point.y == 4
    assert rel_point.z == 5
    
    # Test with list of points
    points = [Point(x=0, y=0, z=0), Point(x=1, y=1, z=1)]
    rel_point = relative_point(points, 1, 1, 1)
    assert rel_point.x == 2
    assert rel_point.y == 2
    assert rel_point.z == 2
    
    # Test invalid reference
    with pytest.raises(Exception) as exc_info:
        relative_point(Point(x=1, y=None, z=1), 1, 1, 1)
    assert "must have all of x, y, z attributes defined" in str(exc_info.value)

def test_flatten():
    # Test flattening nested lists
    nested = [[1, 2], [3, 4], 5, [6, 7]]
    result = flatten(nested)
    assert result == [1, 2, 3, 4, 5, 6, 7]
    
    # Test with Point objects
    p1 = Point(x=1, y=1)
    p2 = Point(x=2, y=2)
    nested = [[p1], p2]
    result = flatten(nested)
    assert len(result) == 2
    assert all(isinstance(p, Point) for p in result)

def test_linspace():
    # Test basic linspace
    result = linspace(0, 10, 5)
    assert len(result) == 5
    assert result[0] == 0
    assert result[-1] == 10
    assert result[2] == 5  # Middle point
    
    # Test with negative numbers
    result = linspace(-5, 5, 3)
    assert result[0] == -5
    assert result[1] == 0
    assert result[2] == 5

def test_first_and_last_point():
    # Create test points
    p1 = Point(x=1, y=1, z=None)
    p2 = Point(x=2, y=2, z=2)
    p3 = Point(x=3, y=3, z=3)
    steps = [p1, "not a point", p2, p3]
    
    # Test first_point with fully_defined=True
    result = first_point(steps, fully_defined=True)
    assert result == p2
    
    # Test first_point with fully_defined=False
    result = first_point(steps, fully_defined=False)
    assert result == p1
    
    # Test last_point
    result = last_point(steps, fully_defined=True)
    assert result == p3
    
    # Test empty list
    with pytest.raises(Exception):
        first_point([], fully_defined=True)
    with pytest.raises(Exception):
        last_point([], fully_defined=True)