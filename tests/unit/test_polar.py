import pytest
from fullcontrol.geometry.polar import polar_to_point, point_to_polar, polar_to_vector, PolarPoint
from fullcontrol.point import Point
from fullcontrol.geometry.vector import Vector
from math import pi, isclose, tau

def test_polar_to_point():
    # Test conversion from polar to cartesian coordinates
    center = Point(x=1, y=1, z=1)
    
    # Test at 0 degrees (along x-axis)
    point = polar_to_point(center, radius=2, angle=0)
    assert isclose(point.x, 3, rel_tol=1e-6)  # center.x + radius
    assert isclose(point.y, 1, rel_tol=1e-6)  # center.y
    assert point.z == center.z
    
    # Test at 90 degrees (along y-axis)
    point = polar_to_point(center, radius=2, angle=pi/2)
    assert isclose(point.x, 1, rel_tol=1e-6)  # center.x
    assert isclose(point.y, 3, rel_tol=1e-6)  # center.y + radius
    assert point.z == center.z

def test_point_to_polar():
    # Test conversion from cartesian to polar coordinates
    origin = Point(x=0, y=0, z=0)
    
    # Test point on x-axis
    point = Point(x=2, y=0, z=0)
    polar = point_to_polar(point, origin)
    assert isclose(polar.radius, 2, rel_tol=1e-6)
    assert isclose(polar.angle, 0, rel_tol=1e-6)
    
    # Test point on y-axis
    point = Point(x=0, y=2, z=0)
    polar = point_to_polar(point, origin)
    assert isclose(polar.radius, 2, rel_tol=1e-6)
    assert isclose(polar.angle, pi/2, rel_tol=1e-6)
    
    # Test point in second quadrant
    point = Point(x=-1, y=1, z=0)
    polar = point_to_polar(point, origin)
    assert isclose(polar.radius, 2**0.5, rel_tol=1e-6)
    assert isclose(polar.angle % tau, (3*pi/4) % tau, rel_tol=1e-6)

def test_polar_to_vector():
    # Test conversion from polar coordinates to vector
    
    # Test along x-axis
    vector = polar_to_vector(length=2, angle=0)
    assert isclose(vector.x, 2, rel_tol=1e-6)
    assert isclose(vector.y, 0, rel_tol=1e-6)
    
    # Test along y-axis
    vector = polar_to_vector(length=2, angle=pi/2)
    assert isclose(vector.x, 0, rel_tol=1e-6)
    assert isclose(vector.y, 2, rel_tol=1e-6)
    
    # Test 45 degrees
    vector = polar_to_vector(length=2**0.5, angle=pi/4)
    assert isclose(vector.x, 1, rel_tol=1e-6)
    assert isclose(vector.y, 1, rel_tol=1e-6)

def test_polar_point():
    # Test PolarPoint model
    polar = PolarPoint(radius=2, angle=pi/2)
    assert polar.radius == 2
    assert polar.angle == pi/2
    
    # Test validation
    with pytest.raises(Exception):
        PolarPoint(radius="invalid", angle=0)  # radius must be float
    with pytest.raises(Exception):
        PolarPoint(radius=2, angle="invalid")  # angle must be float