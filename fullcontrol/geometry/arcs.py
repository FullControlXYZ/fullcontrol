from fullcontrol.common import linspace
from fullcontrol.geometry import Point, polar_to_point, ramp_xyz, ramp_polar
from math import tau, sin, cos

def _clean_float(x: float, epsilon: float = 1e-10) -> float:
    """Clean up floating point values that are very close to 0."""
    return 0.0 if abs(x) < epsilon else x

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
    points = [polar_to_point(centre, radius, a) for a in a_steps]
    # Clean up floating point errors
    for p in points:
        p.x = _clean_float(p.x)
        p.y = _clean_float(p.y)
    return points


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
    points = [Point(
        x=_clean_float(a*cos(t) + centre.x), 
        y=_clean_float(b*sin(t) + centre.y), 
        z=centre.z
    ) for t in t_steps]
    return points
