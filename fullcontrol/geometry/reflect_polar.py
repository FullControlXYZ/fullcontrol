
from fullcontrol.geometry import Point, reflectXY, polar_to_point


def reflectXYpolar(p: Point, p_reflect: Point, angle_reflect: float) -> Point:
    'reflect x and y values of a point about a line defined by a point and polar angle (radians). return new point with original z'
    return reflectXY(p, p_reflect, polar_to_point(p_reflect, 1, angle_reflect))
