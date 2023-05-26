
from fullcontrol import Point, Extruder, PrinterCommand, point_to_polar, polar_to_point
from lab.fullcontrol.geometry.bezier import bezier
# from fullcontrol.geometry import point_to_polar, polar_to_point


def loop_between_lines(point_a1: Point, point_a2: Point, point_b1: Point, point_b2: Point, extension: float, travel: bool = False, retract: bool = False, num_points: int = 10, linearity: int = 0) -> list:
    ''' move along a bezier curve to get from the end of one line to the beginning of the next line. 
    first line defined by point_a1 and point_a2. second line defined by point_b1 and point_b2. 
    bezier starts at point_a2, ends at point_b1, and has control points that are directly 
    extended from lines a and b by the distance of the 'extension' parameter. 'linearity' (0 to 10) 
    defines how close the loop gets to the control points (10 = directly through them). returns a 
    list of fc.Points if travel=False, otherwise, returns a list of points and fc.Extruders to turn 
    extrusion off at point_a2 and on at point_b1 (with retraction if retract=True).
    '''
    polar_a = point_to_polar(point_a2, point_a1)
    point_a3 = polar_to_point(point_a2, extension, polar_a.angle)  # point_a3 is the extended point of the line a1-a2
    polar_b = point_to_polar(point_b1, point_b2)
    point_b0 = polar_to_point(point_b1, extension, polar_b.angle)  # point_b0 is the extended point of the line b1-b2 (extended backwards)
    if linearity == 10:  # if 'linearity' is max, print directly through extended points, otherwise use a bezier curve
        loop_steps = [point_a2, point_a3, point_b0, point_b1]
    else:
        # to make the bezier curve more linear, add extra identical control points (number of extra points = 'linearity')
        loop_steps = bezier([point_a2] + [point_a3]*(1+linearity) + [point_b0]*(1+linearity) + [point_b1], num_points)
    if travel:  # turn extrusion off/on before/after the bezier curve if travel==True
        loop_steps.insert(0, Extruder(on=False))
        loop_steps.append(Extruder(on=True))
    if retract:  # include retraction/unretraction if retraction==True
        loop_steps.insert(0, PrinterCommand(id='retract'))
        loop_steps.append(PrinterCommand(id='unretract'))
    return loop_steps
