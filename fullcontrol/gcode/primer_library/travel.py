
from fullcontrol.gcode import Point, Extruder
from copy import deepcopy

def primer(end_point: Point) -> list:
    'travel to "end_point", which should coincide with the main procedure start point'
    primer_steps = []
    primer_steps.append(Extruder(on=False))
    primer_steps.append(deepcopy(end_point))  # move fast to start position
    primer_steps.append(Extruder(on=True))
    return primer_steps
