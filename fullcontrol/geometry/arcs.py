
from fullcontrol.common import linspace
from fullcontrol.geometry import Point, polar_to_point, ramp_xyz, ramp_polar
from fullcontrol.geometry.midpoint import centreXY_3pt
from math import tau, sin , cos


def arcXY(centre: Point, radius: float, start_angle: float, arc_angle: float, segments: int = 100) -> list:
    '''Generate a 2D-XY arc with angles defined in radians and z-position the same as that of the centre point.
    
    Args:
        centre (Point): The center point of the arc.
        radius (float): The radius of the arc.
        start_angle (float): The starting angle (radians) of the arc.
        arc_angle (float): The angle (radians) of the arc.
        segments (int, optional): The number of segments to divide the arc into. Defaults to 100.
    
    Returns:
        list: A list of Points representing the arc.
    '''
    a_steps = linspace(start_angle, start_angle+arc_angle, segments+1)
    return [polar_to_point(centre, radius, a) for a in a_steps]


def variable_arcXY(centre: Point, start_radius: float, start_angle: float, arc_angle: float, segments: int = 100, radius_change: float = 0, z_change: float = 0) -> list:
    '''Generate a arc with optionally varying radius and z-position. angles are defined in radians. z-position starts the same as that of the centre point and increased by z_change.

    Parameters:
    - centre (Point): The centre point of the arc.
    - start_radius (float): The starting radius of the arc.
    - start_angle (float): The starting polar angle (radians) of the arc.
    - arc_angle (float): The angle (radians) of the arc.
    - segments (int, optional): The number of segments to divide the arc into (default is 100).
    - radius_change (float, optional): The optional change in radius of the arc (default is 0).
    - z_change (float, optional): The optional change in z-position of the arc (default is 0).

    Returns:
    - list: A list of Points representing the variable arc.

    '''
    arc = arcXY(centre, start_radius, start_angle, arc_angle, segments)  # create arc with constant radius and z
    arc = ramp_xyz(arc, z_change=z_change)  # ramp z of the arc
    # ramp radius of the arc
    return ramp_polar(arc, centre, radius_change=radius_change)


def elliptical_arcXY(centre: Point, a: float, b: float, start_angle: float, arc_angle: float, segments: int = 100) -> list:
    '''Generate a 2D-XY elliptical arc with z-position the same as that of the centre point
    Args:
        centre (Point): The centre point of the arc.
        a (float): The x-width of the ellipse.
        b (float): The y-height of the ellipse.
        start_angle (float): The starting polar angle of the arc in radians.
        arc_angle (float): The angle of the arc in radians.
        segments (int, optional): The number of segments to divide the arc into. Defaults to 100.
    
    Returns:
        list: A list of Points representing the elliptical arc.
    '''
    
    t_steps = linspace(start_angle, start_angle+arc_angle, segments+1)
    return [Point(x=a*cos(t) + centre.x, y=b*sin(t) + centre.y, z=centre.z) for t in t_steps]


def arcXY_3pt(pt1: Point, pt2: Point, pt3: Point, segments: int = 100) -> list:
    '''Generate a 2D-XY arc passing through three specified points.
    
    Args:
        pt1 (Point): The starting point of the arc.
        pt2 (Point): An intermediate point that the arc passes through.
        pt3 (Point): The ending point of the arc.
        segments (int, optional): The number of segments to divide the arc into. Defaults to 100.
    
    Returns:
        list: A list of Points representing the arc from pt1 through pt2 to pt3.
    '''
    from math import atan2, pi
    
    centre = centreXY_3pt(pt1, pt2, pt3)
    radius = ((pt1.x - centre.x)**2 + (pt1.y - centre.y)**2)**0.5
    
    start_angle = atan2(pt1.y - centre.y, pt1.x - centre.x)
    mid_angle = atan2(pt2.y - centre.y, pt2.x - centre.x)
    end_angle = atan2(pt3.y - centre.y, pt3.x - centre.x)
    
    # Normalize angles and determine direction
    for angle in [start_angle, mid_angle, end_angle]:
        while angle < 0: angle += 2*pi
        while angle >= 2*pi: angle -= 2*pi
    
    # Determine arc direction and angle
    ccw = (mid_angle > start_angle and mid_angle < end_angle) or (start_angle > end_angle and (mid_angle > start_angle or mid_angle < end_angle))
    arc_angle = end_angle - start_angle if ccw else -(2*pi - (end_angle - start_angle))
    
    return arcXY(centre, radius, start_angle, arc_angle, segments)
