
from fullcontrol.geometry import Point, Vector
from copy import deepcopy
from typing import Union


def move(geometry: Union[Point, list], vector: Vector, copy: bool = False, copy_quantity: int = 2) -> Union[Point, list]:
    '''move 'geometry' (a Point or list of steps including Points) by 'vector'. 
    elements in a list that are not Points pass through and are replicated without 
    modification. if copy==True, multiple copies of 'geometry' are created, each 
    offset by 'vector' from the previous copy. 'copy_quantity' includes the position 
    of the original geometry. return the new geometry as a list (original geometry 
    is not edited).
    '''
    if copy:
        return copy_geometry(geometry, vector, copy_quantity)
    else:
        return move_geometry(geometry, vector)


def move_geometry(geometry: Union[Point, list], vector: Vector) -> Union[Point, list]:
    '''move 'geometry' (a Point or list of steps including Points) by 'vector' 
    and return the moved geometry (original geometry is not edited). elements 
    in a list that are not Points pass through without modification
    '''

    def move_point(point: Point, vector: Vector) -> Point:
        'return a copy of a the given point, offset by the given vector'
        point_new = deepcopy(point)  # deepcopy so that color attribute is copied
        if point_new.x != None and vector.x != None:
            point_new.x += vector.x
        if point_new.y != None and vector.y != None:
            point_new.y += vector.y
        if point_new.z != None and vector.z != None:
            point_new.z += vector.z
        return point_new
    if isinstance(geometry, Point):
        return move_point(geometry, vector)
    else:
        geometry_new = []
        for element in geometry:
            if isinstance(element, Point):
                geometry_new.append(move_point(element, vector))
            else:
                geometry_new.append(element)
        return geometry_new


def copy_geometry(geometry: Union[Point, list], vector: Vector, quantity: int) -> list:
    '''creates multiple copies of 'geometry' (a Point or list of steps including 
    Points), each offset by 'vector' from the previous copy. elements in a list 
    that are not Points pass through and are replicated without modification. 
    'quantity' includes the position of the original geometry. return the new 
    geometry as a list (original geometry is not edited). 
    '''
    steps_new = []
    for i in range(quantity):
        v_now = Vector()
        v_now.x = vector.x*i if vector.x != None else None
        v_now.y = vector.y*i if vector.y != None else None
        v_now.z = vector.z*i if vector.z != None else None
        if isinstance(geometry, Point):
            steps_new.append(move_geometry(geometry, v_now))
        else:
            steps_new.extend(move_geometry(geometry, v_now))
    return steps_new
