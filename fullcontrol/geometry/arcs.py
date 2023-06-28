
from fullcontrol.common import linspace
from fullcontrol.geometry import Point, polar_to_point, ramp_xyz, ramp_polar
from math import tau, sin , cos


def arcXY(centre: Point, radius: float, start_angle: float, arc_angle: float, segments: int = 100) -> list:
    '''generate 2d-xy arc with the specified number of segments, centred about a point, with the given radius,
    given arc angle (radians), starting at the specified polar angle (radians), with z-position the same as that
    of the centre point. return list of Points
    '''
    a_steps = linspace(start_angle, start_angle+arc_angle, segments+1)
    return [polar_to_point(centre, radius, a) for a in a_steps]


def variable_arcXY(centre: Point, start_radius: float, start_angle: float, arc_angle: float, segments: int = 100, radius_change: float = 0, z_change: float = 0) -> list:
    '''generate a variable arc with the specified number of segments, centred about a point, for the given arc angle (radians), 
    starting at the specified polar angle (radians), with radius governed by the start radius and optional change in radius, 
    and z-position starting with the centre-point z and optionally increasing by z_change. return list of Points
    '''
    arc = arcXY(centre, start_radius, start_angle, arc_angle, segments)  # create arc with constant radius and z
    arc = ramp_xyz(arc, z_change=z_change)  # ramp z of the arc
    # ramp radius of the arc
    return ramp_polar(arc, centre, radius_change=radius_change)


def arcXY(centre: Point, radius: float, start_angle: float, arc_angle: float, segments: int = 100) -> list:
    '''generate 2d-xy arc with the specified number of segments, centred about a point, with the given radius,
    given arc angle (radians), starting at the specified polar angle (radians), with z-position the same as that
    of the centre point. return list of Points
    '''
    a_steps = linspace(start_angle, start_angle+arc_angle, segments+1)
    return [polar_to_point(centre, radius, a) for a in a_steps]

def elliptical_arcXY(centre: Point, a: float, b: float, start_angle: float, arc_angle: float, segments: int=100) -> list:
    '''generate a 2d-xy elliptical arc with the specified number of segments, centred about a point, 
    for the given a (x-width) and b (y-height), given the arc angle (radians), starting at the specified polar angle (radians), 
    with z-position the same as that of the centre point. return list of Points
    '''
    
    t_steps = linspace(start_angle, start_angle+arc_angle, segments+1)
    return [Point(x=a*cos(t) + centre.x, y=b*sin(t) + centre.y, z=centre.z) for t in t_steps]
