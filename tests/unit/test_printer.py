import pytest
from fullcontrol.printer import Printer

def test_printer_initialization():
    # Test default initialization
    printer = Printer()
    assert printer.print_speed is None
    assert printer.travel_speed is None
    
    # Test initialization with values
    printer = Printer(print_speed=60.0, travel_speed=120.0)
    assert printer.print_speed == 60.0
    assert printer.travel_speed == 120.0
    
    # Test partial initialization
    printer = Printer(print_speed=60.0)
    assert printer.print_speed == 60.0
    assert printer.travel_speed is None

def test_printer_speed_updates():
    printer = Printer()
    
    # Test updating print speed
    printer.print_speed = 30.0
    assert printer.print_speed == 30.0
    
    # Test updating travel speed
    printer.travel_speed = 90.0
    assert printer.travel_speed == 90.0
    
    # Test dictionary-style access
    printer["print_speed"] = 45.0
    assert printer.print_speed == 45.0
    assert printer["print_speed"] == 45.0