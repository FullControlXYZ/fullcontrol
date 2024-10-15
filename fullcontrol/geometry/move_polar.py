
from fullcontrol.geometry import Point, point_to_polar, polar_to_point
from fullcontrol.check import check_points
from copy import deepcopy
from typing import Union


def move_polar(geometry: Union[Point, list], centre: Point, radius: float, angle: float, copy: bool = False, copy_quantity: int = 2) -> Union[Point, list]:
    '''
    Move 'geometry' (a Point or list of steps including Points) about a 
    centre point by the given radius and angle (in radians) relative to the 
    current radius and angle of each Point.

    All Points must have x and y attributes explicitly defined. Elements in a 
    list that are not Points pass through and are replicated without modification.

    If copy is True, multiple copies of 'geometry' are created, each moved about 
    a centre point by the given radius and angle relative to the radius and angle 
    of each respective point in the previous copy of the geometry.

    Parameters:
        geometry (Union[Point, list]): The geometry to be moved. 
        centre (Point): The centre point about which the geometry is moved.
        radius (float): The radius of movement.
        angle (float): The angle of movement in radians.
        copy (bool, optional): Whether to create multiple copies of the geometry. Defaults to False.
        copy_quantity (int, optional): The number of copies to create. Defaults to 2.

    Returns:
        Union[Point, list]: The new geometry as a list (original geometry is not edited).
    '''
    check_points(geometry, check='polar_xy')
    if copy == False:
        return move_geometry_polar(geometry, centre, radius, angle)
    else:
        return copy_geometry_polar(geometry, centre, radius, angle, copy_quantity)


def move_geometry_polar(geometry: Union[Point, list], centre: Point, radius: float, angle: float) -> Union[Point, list]:
    '''
    Function called by move_polar()
    
    Move 'geometry' (a Point or list of steps including Points) about a 
    centre point by the given radius and angle (radians) relative to the 
    current radius and angle of each Point. Return the moved geometry (original 
    geometry is not edited). Elements in a list that are not Points pass 
    through without modification.

    Parameters:
    - geometry: A Point or a list of steps including Points.
    - centre: The centre point about which the geometry is moved.
    - radius: The radius by which the geometry is moved.
    - angle: The angle (in radians) by which the geometry is moved.

    Returns:
    - The moved geometry, which can be a Point or a list of Points.

    Note:
    - If the input geometry is a Point, it is moved about the centre point by the given radius and angle.
    - If the input geometry is a list, each Point in the list is moved about the centre point by the given radius and angle.
    - Elements in the list that are not Points pass through without modification.
    '''
    def move_point_about_point(point: Point, centre: Point, radius: float, angle: float) -> Point:
        '''Return a copy of the given point, moved about the given centre-point by the given radius-change and angle-change.

        Parameters:
        - point: The point to be moved.
        - centre: The centre point about which the point is moved.
        - radius: The radius by which the point is moved.
        - angle: The angle (in radians) by which the point is moved.

        Returns:
        - The moved point, which is a copy of the original point with updated coordinates.
        '''
        polar_data = point_to_polar(point, centre)
        point_new_xy = polar_to_point(centre, polar_data.radius+radius, polar_data.angle+angle)
        point_new = deepcopy(point)  # deepcopy so that color and z attributes are copied
        point_new.x, point_new.y = point_new_xy.x, point_new_xy.y
        return point_new

    if type(geometry).__name__ == "Point":
        return move_point_about_point(geometry, centre, radius, angle)
    else:
        geometry_new = []
        for i in range(len(geometry)):
            if type(geometry[i]).__name__ == 'Point':
                geometry_new.append(move_point_about_point(geometry[i], centre, radius, angle))
            else:
                geometry_new.append(geometry[i])
        return geometry_new


def copy_geometry_polar(geometry: Union[Point, list], centre: Point, radius: float, angle: float, quantity: int) -> list:
    '''
    Function called by move_polar()
    
    Creates multiple copies of 'geometry' (a Point or list of steps including Points).
    Elements in a list that are not Points pass through and are replicated without modification.
    Each copy is moved about a centre point by the given radius and angle (in radians) relative to the radius and angle of each respective point in the previous copy of the geometry.
    Returns the moved geometry (original geometry is not edited).
    'quantity' includes the position of the original geometry.
    Returns the new geometry as a list (original geometry is not edited).

    Parameters:
        - geometry: The geometry to be copied. It can be a Point or a list of steps including Points.
        - centre: The centre point about which the geometry will be moved.
        - radius: The radius by which the geometry will be moved in each copy.
        - angle: The angle (in radians) by which the geometry will be rotated in each copy.
        - quantity: The number of copies to be created, including the position of the original geometry.

    Returns:
        A list containing the moved geometry.
    '''
    steps_new = []
    for i in range(quantity):
        radius_now = radius * i
        angle_now = angle * i
        if type(geometry).__name__ == "Point":
            steps_new.append(move_geometry_polar(geometry, centre, radius_now, angle_now))
        else:
            steps_new.extend(move_geometry_polar(geometry, centre, radius_now, angle_now))
    return steps_new
