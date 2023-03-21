
from fullcontrol.gcode import Point, Extruder
from fullcontrol.gcode import ManualGcode


def primer(end_point: Point) -> list:
    'returns an empty list for the primer steps. no primer is desired, but a list object is needed for consistency'
    primer_steps = []
    return primer_steps
