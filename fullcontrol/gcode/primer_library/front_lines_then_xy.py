
from fullcontrol.gcode import Point, Extruder
from fullcontrol.gcode import ManualGcode


def primer(end_point: Point) -> list:
    'prints primer lines at front of bed then prints in diagonal xy direction to "end_point", which should coincide with the main procedure start point'
    primer_steps = []
    primer_steps.append(ManualGcode(text=';-----\n; START OF PRIMER PROCEDURE\n;-----'))
    primer_steps.append(Extruder(on=False))
    primer_steps.append(Point(x=10, y=12, z=end_point.z))  # move fast to start z
    primer_steps.append(Extruder(on=True))
    # print a rectangle to prime the nozzle
    primer_steps.append(Point(x=110))
    primer_steps.append(Point(y=14))
    primer_steps.append(Point(x=10))
    primer_steps.append(Point(y=16))
    primer_steps.append(Point(x=end_point.x, y=end_point.y))  # print to start xy
    primer_steps.append(ManualGcode(text=';-----\n; END OF PRIMER PROCEDURE\n;-----\n'))
    return primer_steps
