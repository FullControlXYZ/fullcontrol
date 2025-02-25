import pytest
from fullcontrol.extrusion_classes import ExtrusionGeometry, StationaryExtrusion, Extruder
from math import pi, isclose

def test_extrusion_geometry_rectangle():
    geom = ExtrusionGeometry(area_model="rectangle", width=2.0, height=1.0)
    geom.update_area()
    assert geom.area == 2.0  # width * height

def test_extrusion_geometry_stadium():
    geom = ExtrusionGeometry(area_model="stadium", width=4.0, height=2.0)
    geom.update_area()
    # Stadium area = (width - height) * height + π * (height/2)²
    expected_area = (4.0 - 2.0) * 2.0 + pi * (2.0/2)**2
    assert isclose(geom.area, expected_area, rel_tol=1e-9)

def test_extrusion_geometry_circle():
    geom = ExtrusionGeometry(area_model="circle", diameter=2.0)
    geom.update_area()
    # Circle area = π * (diameter/2)²
    expected_area = pi * (2.0/2)**2
    assert isclose(geom.area, expected_area, rel_tol=1e-9)

def test_extrusion_geometry_manual():
    geom = ExtrusionGeometry(area_model="manual", area=5.0)
    geom.update_area()
    assert geom.area == 5.0  # Manual area should remain unchanged

def test_stationary_extrusion():
    # Test normal extrusion
    extrusion = StationaryExtrusion(volume=10.0, speed=100)
    assert extrusion.volume == 10.0
    assert extrusion.speed == 100
    
    # Test retraction (negative volume)
    retraction = StationaryExtrusion(volume=-5.0, speed=50)
    assert retraction.volume == -5.0
    assert retraction.speed == 50

def test_extruder():
    # Test extruder on/off states
    extruder = Extruder(on=True)
    assert extruder.on is True
    
    extruder.on = False
    assert extruder.on is False
    
    # Test default state
    default_extruder = Extruder()
    assert default_extruder.on is None