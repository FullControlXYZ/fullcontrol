import pytest
from fullcontrol.check import check_points
from fullcontrol.point import Point

def test_check_points_polar_xy():
    # Test valid point
    valid_point = Point(x=1.0, y=2.0)
    check_points(valid_point, 'polar_xy')  # Should not raise
    
    # Test invalid point with missing x
    invalid_point = Point(y=2.0)
    with pytest.raises(Exception) as exc_info:
        check_points(invalid_point, 'polar_xy')
    assert "polar transformations can only be applied to points" in str(exc_info.value)
    
    # Test invalid point with missing y
    invalid_point = Point(x=1.0)
    with pytest.raises(Exception) as exc_info:
        check_points(invalid_point, 'polar_xy')
    assert "polar transformations can only be applied to points" in str(exc_info.value)
    
    # Test list of points
    points = [
        Point(x=1.0, y=2.0),
        Point(x=3.0, y=4.0)
    ]
    check_points(points, 'polar_xy')  # Should not raise
    
    # Test list with invalid point
    invalid_points = [
        Point(x=1.0, y=2.0),
        Point(x=3.0)  # Missing y
    ]
    with pytest.raises(Exception) as exc_info:
        check_points(invalid_points, 'polar_xy')
    assert "polar transformations can only be applied to points" in str(exc_info.value)

def test_check_points_invalid_check_type():
    point = Point(x=1.0, y=2.0)
    with pytest.raises(Exception) as exc_info:
        check_points(point, 'invalid_check')
    # The function should raise an exception for invalid check type