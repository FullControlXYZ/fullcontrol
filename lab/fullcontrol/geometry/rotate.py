import math
from fullcontrol.geometry import Point
from typing import Union
from copy import deepcopy
from math import sqrt, cos, sin, radians


def dot_product(v1, v2):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z


def cross_product(v1, v2):
    return Point(x=v1.y*v2.z - v1.z*v2.y, y=v1.z*v2.x - v1.x*v2.z, z=v1.x*v2.y - v1.y*v2.x)


def rotate(geometry: Union[Point, list], axis_start: Point, axis_end_or_direction: Union[Point, str], angle_rad: float, copy: bool = False, copy_quantity: int = 2) -> Union[Point, list]:
    '''rotate 'geometry' (a Point or list of steps including Points) about an axis 
    by a defined angle (radians). the axis is defined by two points for the axis_start 
    and axis_end or by one point for axis_start and a direction 'x', 'y' or 'z'.
    elements in a list that are not Points pass through and are replicated without
    modification. if copy==True, multiple copies of 'geometry' are created, each
    offset by 'vector' from the previous copy. 'copy_quantity' includes the position
    of the original geometry. return the new geometry as a list (original geometry
    is not edited).
    '''
    if isinstance(axis_end_or_direction, Point):
        axis_end = axis_end_or_direction
    elif axis_end_or_direction == 'x':
        axis_end = Point(x=axis_start.x+1, y=axis_start.y, z=axis_start.z)
    elif axis_end_or_direction == 'y':
        axis_end = Point(x=axis_start.x, y=axis_start.y+1, z=axis_start.z)
    elif axis_end_or_direction == 'z':
        axis_end = Point(x=axis_start.x, y=axis_start.y, z=axis_start.z+1)

    if copy:
        return rotate_copy_geometry(geometry, axis_start, axis_end, angle_rad, copy_quantity)
    else:
        return rotate_geometry(geometry, axis_start, axis_end, angle_rad)


def rotate_geometry(geometry: Union[Point, list], axis_start: Point, axis_end: Point, angle_rad: float) -> Union[Point, list]:
    '''rotate 'geometry' (a Point or list of steps including Points) 
    about the given axis by the given angle' and return the rotated 
    geometry (original geometry is not edited). elements in a list. 
    Objects that are not Points pass through without modification
    '''

    def rotate_point(point: Point, axis_start: Point, axis_end: Point, angle_rad: float) -> Point:
        'return a copy of a the given point, rotated about the given axis by the given angle'
        point_new = deepcopy(point)  # deepcopy so that color attribute is copied

        # Vector along the rotation axis
        axis = Point(x=axis_end.x - axis_start.x, y=axis_end.y - axis_start.y, z=axis_end.z - axis_start.z)

        # Normalize the rotation axis vector
        norm = sqrt(axis.x**2 + axis.y**2 + axis.z**2)
        axis = Point(x=axis.x/norm, y=axis.y/norm, z=axis.z/norm)

        # offset to be relative to origin
        point_new.x -= axis_start.x
        point_new.y -= axis_start.y
        point_new.z -= axis_start.z

        # Rodrigues' rotation formula to find point rotated about vector through origin
        rotated_x = point_new.x*cos(angle_rad) + cross_product(axis, point_new).x*sin(angle_rad) + \
            axis.x*dot_product(axis, point_new)*(1 - cos(angle_rad))
        rotated_y = point_new.y*cos(angle_rad) + cross_product(axis, point_new).y*sin(angle_rad) + \
            axis.y*dot_product(axis, point_new)*(1 - cos(angle_rad))
        rotated_z = point_new.z*cos(angle_rad) + cross_product(axis, point_new).z*sin(angle_rad) + \
            axis.z*dot_product(axis, point_new)*(1 - cos(angle_rad))

        # offset away from origin
        point_new.x = rotated_x + axis_start.x
        point_new.y = rotated_y + axis_start.y
        point_new.z = rotated_z + axis_start.z

        return point_new

    if isinstance(geometry, Point):
        return rotate_point(geometry, axis_start, axis_end, angle_rad)
    else:
        geometry_new = []
        for element in geometry:
            if isinstance(element, Point):
                geometry_new.append(rotate_point(element, axis_start, axis_end, angle_rad))
            else:
                geometry_new.append(element)
        return geometry_new


def rotate_copy_geometry(geometry: Union[Point, list], axis_start: Point, axis_end: Point, angle_rad: float, quantity: int) -> list:
    '''creates multiple copies of 'geometry' (a Point or list of steps including
    Points), each rotated about the given axis by the given angle. elements in a list
    that are not Points pass through and are replicated without modification.
    'quantity' includes the position of the original geometry. return the new
    geometry as a list (original geometry is not edited).
    '''
    steps_new = []
    for i in range(quantity):
        angle_now = angle_rad*i
        if isinstance(geometry, Point):
            steps_new.append(rotate_geometry(geometry, axis_start, axis_end, angle_now))
        else:
            steps_new.extend(rotate_geometry(geometry, axis_start, axis_end, angle_now))
    return steps_new
