
from fullcontrol.geometry import Point, Vector
from copy import deepcopy
from typing import Union


def move(geometry: Union[Point, list], vector: Vector, copy: bool = False, copy_quantity: int = 2) -> Union[Point, list]:
    '''
    Move 'geometry' (a Point or list of steps including Points) by 'vector'.

    If 'geometry' is a Point, it is moved by 'vector' and the new Point is returned.
    If 'geometry' is a list, each element in the list is checked. If an element is a Point,
    it is moved by 'vector'. If an element is not a Point, it is passed through without modification.
    The modified list is returned.

    If 'copy' is True, multiple copies of 'geometry' are created, each offset by 'vector' from the previous copy.
    The total number of copies is determined by 'copy_quantity', which includes the position of the original geometry.
    The new geometries are returned as a list, with the original geometry not being modified.

    Parameters:
        geometry (Union[Point, list]): The geometry to be moved. It can be a Point or a list of Points.
        vector (Vector): The vector by which the geometry should be moved.
        copy (bool, optional): If True, multiple copies of the geometry are created. Defaults to False.
        copy_quantity (int, optional): The number of copies to be created. Defaults to 2.

    Returns:
        Union[Point, list]: The new geometry after being moved. If 'geometry' is a Point, a new Point is returned.
        If 'geometry' is a list, a new list with the modified Points is returned.
    '''
    if copy:
        return copy_geometry(geometry, vector, copy_quantity)
    else:
        return move_geometry(geometry, vector)


def move_geometry(geometry: Union[Point, list], vector: Vector) -> Union[Point, list]:
    '''
    Function called by move()
    
    Move 'geometry' (a Point or list of steps including Points) by 'vector' 
    and return the moved geometry (original geometry is not edited). Elements 
    in a list that are not Points pass through without modification.

    Parameters:
        geometry (Union[Point, list]): The geometry to be moved. It can be a single Point or a list of Points.
        vector (Vector): The vector by which the geometry should be moved.

    Returns:
        Union[Point, list]: The moved geometry. If the input is a single Point, the function returns a new Point object.
        If the input is a list of Points, the function returns a new list with the moved Points and the other elements unchanged.
    '''
    def move_point(point: Point, vector: Vector) -> Point:
        '''
        Return a copy of the given point, offset by the given vector.

        Parameters:
            point (Point): The point to be moved.
            vector (Vector): The vector by which the point should be moved.

        Returns:
            Point: A new Point object with the updated coordinates.
        '''
        point_new = deepcopy(point)  # deepcopy so that color attribute is copied
        if point_new.x is not None and vector.x is not None:
            point_new.x += vector.x
        if point_new.y is not None and vector.y is not None:
            point_new.y += vector.y
        if point_new.z is not None and vector.z is not None:
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
    '''
    Function called by move()
    
    Creates multiple copies of 'geometry' (a Point or list of steps including Points),
    each offset by 'vector' from the previous copy. Elements in a list that are not Points
    pass through and are replicated without modification. 'quantity' includes the position
    of the original geometry. Returns the new geometry as a list (original geometry is not edited).
    
    Parameters:
        - geometry: The geometry to be copied. It can be a Point or a list of steps including Points.
        - vector: The vector by which each copy of the geometry is offset from the previous copy.
        - quantity: The number of copies to be created, including the position of the original geometry.
        
    Returns:
        A list containing the new geometry, with each copy offset by the specified vector.
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
