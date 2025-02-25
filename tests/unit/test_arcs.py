import pytest
from fullcontrol.geometry.arcs import arcXY, variable_arcXY, elliptical_arcXY
from fullcontrol.point import Point
from math import pi, isclose

def test_arcXY():
    """Test basic arc generation"""
    center = Point(x=0, y=0, z=0)
    radius = 10.0
    # Test quarter circle
    points = arcXY(center, radius, 0, pi/2, segments=4)
    
    # Should have 5 points (4 segments + start point)
    assert len(points) == 5
    
    # Check start and end points
    assert isclose(points[0].x, radius, rel_tol=1e-6)  # Start at (r, 0)
    assert isclose(points[0].y, 0, rel_tol=1e-6)
    assert isclose(points[-1].x, 0, rel_tol=1e-6)  # End at (0, r)
    assert isclose(points[-1].y, radius, rel_tol=1e-6)

def test_variable_arcXY():
    """Test arc with varying radius and height"""
    center = Point(x=0, y=0, z=0)
    start_radius = 10.0
    radius_change = 5.0
    z_change = 2.0
    
    points = variable_arcXY(
        center, start_radius, 0, pi/2, segments=4,
        radius_change=radius_change, z_change=z_change
    )
    
    # Should have 5 points
    assert len(points) == 5
    
    # Check start point
    assert isclose(points[0].x, start_radius, rel_tol=1e-6)
    assert isclose(points[0].y, 0, rel_tol=1e-6)
    assert isclose(points[0].z, 0, rel_tol=1e-6)
    
    # Check end point - should have increased radius and height
    end_radius = start_radius + radius_change
    distance_from_center = (points[-1].x**2 + points[-1].y**2)**0.5
    assert isclose(distance_from_center, end_radius, rel_tol=1e-6)
    assert isclose(points[-1].z, z_change, rel_tol=1e-6)

def test_elliptical_arcXY():
    """Test elliptical arc generation"""
    center = Point(x=0, y=0, z=0)
    a = 10.0  # x semi-axis
    b = 5.0   # y semi-axis
    
    points = elliptical_arcXY(center, a, b, 0, pi/2, segments=4)
    
    # Should have 5 points
    assert len(points) == 5
    
    # Check start and end points
    assert isclose(points[0].x, a, rel_tol=1e-6)  # Start at (a, 0)
    assert isclose(points[0].y, 0, rel_tol=1e-6)
    
    assert isclose(points[-1].x, 0, rel_tol=1e-6)  # End at (0, b)
    assert isclose(points[-1].y, b, rel_tol=1e-6)
    
    # Z coordinate should remain constant
    for point in points:
        assert point.z == center.z