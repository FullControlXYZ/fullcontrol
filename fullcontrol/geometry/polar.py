
from fullcontrol.geometry import Point, Vector
from math import atan2, cos, sin, tau
from fullcontrol.check import check_points
from pydantic import BaseModel


class PolarPoint(BaseModel):
    """
    Represents a point in polar coordinates.

    Attributes:
        radius (float): The distance from the origin to the point.
        angle (float): The angle between the positive x-axis and the line segment connecting the origin and the point.
    """
    radius: float
    angle: float


def polar_to_point(centre: Point, radius: float, angle: float) -> Point:
    '''
    Convert polar coordinates to Cartesian coordinates.
    Point XY coordinates of a point based on polar angle (radians) and radius from a centre point. The new Point has z = centre.z'

    Args:
        centre (Point): The center point.
        radius (float): The radius.
        angle (float): The angle (radians).

    Returns:
        Point: A new Point object with x, y, and z coordinates calculated based on the given polar coordinates.
    '''
    return Point(x=centre.x + radius*cos(angle), y=centre.y + radius*sin(angle), z=centre.z)


def point_to_polar(target_point: Point, origin_point: Point) -> PolarPoint:
    '''
    Convert a Cartesian point to polar coordinates.
    Find polar radius and angle (radians: 0 to 2pi) in XY plane of the given target point relative 
    to a given origin Point.

    Args:
        target_point (Point): The target point in Cartesian coordinates.
        origin_point (Point): The origin point in Cartesian coordinates.

    Returns:
        PolarPoint: The polar coordinates of the target point relative to the origin point, accessed with .radius and .angle
    '''
    check_points([target_point, origin_point], check='polar_xy')
    r = ((target_point.x - origin_point.x) ** 2 + (target_point.y - origin_point.y) ** 2) ** 0.5
    angle = atan2((target_point.y - origin_point.y), (target_point.x - origin_point.x))
    return PolarPoint(radius=r, angle=angle % tau)


def polar_to_vector(length: float, angle: float) -> Vector:
    '''
    Convert polar coordinates to a vector.
    Find an xy Vector based on an angle (radians) and length defined in polar coordinates.

    Args:
        length (float): The length of the vector.
        angle (float): The angle (in radians) of the vector.

    Returns:
        Vector: A vector with x and y components.

    '''
    pt = polar_to_point(Point(x=0, y=0), length, angle)
    return Vector(x=pt.x, y=pt.y)
