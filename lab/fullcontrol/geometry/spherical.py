
from fullcontrol.geometry import Point, Vector
from math import acos, cos, sin, tau, atan, atan2

from pydantic import BaseModel


class SphericalPoint(BaseModel):
    radius: float
    angle_xy: float  # aka  angle in XY plane - zero if oriented in +x
    angle_z: float  # aka inclination angle - zero if oriented in +z


def spherical_to_point(origin: Point, radius: float, angle_xy: float, angle_z: float) -> Point:
    '''find x y z coordinates of a Point based on the angle in xy plane (zero means
    oriented towards +x), the angle 'down' from the z axis (zero means oriented in Z)
    and the radius. all angles are in radians. returns a Point'''
    return Point(x=origin.x + radius*sin(angle_z)*cos(angle_xy), y=origin.y+radius*sin(angle_z)*sin(angle_xy), z=origin.z + radius*cos(angle_z))


def point_to_spherical(origin_point: Point, target_point: Point) -> SphericalPoint:
    ''''find spherical coordiantes (radius, angle_xy and angle_z) for a Point relative to a 
    given origin Point. angle_xy is zero if oriented towards +x. angle_z is zero if oriented 
    towards +z. return a SphericalPoint, accessed with .radius, .angle_xy and .angle_z '''
    r = ((target_point.x - origin_point.x) ** 2 + (target_point.y - origin_point.y) ** 2 + (target_point.z - origin_point.z) ** 2) ** 0.5
    # angle_xy = acos((target_point.x - origin_point.x)/r)
    # angle_z = acos((target_point.x - origin_point.x)/(r*sin(angle_xy))) breaks sometimes - not sure exactly when
    # angle_xy = atan((target_point.y - origin_point.y)/(target_point.x - origin_point.x)) # breaks if points have identical x values
    # angle_z = atan((((target_point.x - origin_point.x) ** 2 + (target_point.y - origin_point.y) ** 2)**0.5)/(target_point.z - origin_point.z))
    angle_z = acos((target_point.z - origin_point.z) / r)
    angle_xy = atan2((target_point.y - origin_point.y), (target_point.x - origin_point.x))
    return SphericalPoint(radius=r, angle_xy=angle_xy % tau, angle_z=angle_z)


def spherical_to_vector(length: float, angle_xy: float, angle_z: float) -> Vector:
    'return an xy Vector based on spherical coordinates. return a Vector'
    pt = spherical_to_point(Point(x=0, y=0, z=0), length, angle_xy, angle_z)
    return Vector(x=pt.x, y=pt.y, z=pt.z)

# the following function should likely exist in measure.py when this sperical stuff is moved from lab to fullcontrol


def angleZ(start_point: Point, end_point: Point) -> float:
    ' return the angle (radians) of a line down from the Z axis'
    return point_to_spherical(start_point, end_point).angle_z
