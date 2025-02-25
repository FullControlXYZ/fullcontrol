import pytest
from fullcontrol.auxilliary_components import Fan, Hotend, Buildplate

def test_fan():
    # Test default initialization
    fan = Fan()
    assert fan.speed_percent is None
    
    # Test with speed
    fan = Fan(speed_percent=75)
    assert fan.speed_percent == 75
    
    # Test speed updates
    fan.speed_percent = 100
    assert fan.speed_percent == 100
    
    # Test invalid speed values (should be handled by Pydantic validation)
    with pytest.raises(Exception):
        Fan(speed_percent=101)  # Over 100%
    with pytest.raises(Exception):
        Fan(speed_percent=-1)   # Negative percentage

def test_hotend():
    # Test default initialization
    hotend = Hotend()
    assert hotend.temp is None
    assert hotend.wait is False
    assert hotend.tool is None
    
    # Test full initialization
    hotend = Hotend(temp=200, wait=True, tool=0)
    assert hotend.temp == 200
    assert hotend.wait is True
    assert hotend.tool == 0
    
    # Test partial initialization
    hotend = Hotend(temp=180)
    assert hotend.temp == 180
    assert hotend.wait is False
    assert hotend.tool is None
    
    # Test attribute updates
    hotend.temp = 210
    hotend.wait = True
    assert hotend.temp == 210
    assert hotend.wait is True

def test_buildplate():
    # Test default initialization
    buildplate = Buildplate()
    assert buildplate.temp is None
    assert buildplate.wait is False
    
    # Test full initialization
    buildplate = Buildplate(temp=60, wait=True)
    assert buildplate.temp == 60
    assert buildplate.wait is True
    
    # Test partial initialization and updates
    buildplate = Buildplate(temp=50)
    assert buildplate.temp == 50
    assert buildplate.wait is False
    
    buildplate.wait = True
    assert buildplate.wait is True
    
    # Test dictionary-style access
    buildplate["temp"] = 70
    assert buildplate.temp == 70
    assert buildplate["temp"] == 70