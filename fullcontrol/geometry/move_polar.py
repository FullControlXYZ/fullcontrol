
from fullcontrol.geometry import Point, point_to_polar, polar_to_point
from copy import deepcopy
from typing import Union


def move_polar(geometry: Union[Point, list], centre: Point, radius: float, angle: float, copy: bool = False, copy_quantity: int = 2) -> Union[Point, list]:
    ''''move 'geometry' (a Point or list of steps including Points) about a 
    centre point by the given radius and angle (radians) relative to the 
    current radius and angle of each Point. All Points must have x and y 
    attributes explicitly defined. elements in a list that are not Points
    pass through and are replicated without modification. if copy==True, 
    multiple copies of 'geometry' are created, each moved about a centre point 
    by the given radius and angle relative to the radius and angle of each 
    respective point in the previous copy of the geometry.'copy_quantity' includes 
    the position of the original geometry. return the new geometry as a list 
    (original geometry is not edited).
    '''
    if copy == False:
        return move_geometry_polar(geometry, centre, radius, angle)
    else:
        return copy_geometry_polar(geometry, centre, radius, angle, copy_quantity)


def move_geometry_polar(geometry: Union[Point, list], centre: Point, radius: float, angle: float) -> Union[Point, list]:
    ''''move 'geometry' (a Point or list of steps including Points) about a 
    centre point by the given radius and angle (radians) relative to the 
    current radius and angle of each Point. return the moved geometry (original 
    geometry is not edited). elements in a list that are not Points pass 
    through without modification
    '''
    def move_point_about_point(point: Point, centre: Point, radius: float, angle: float) -> Point:
        'return a copy of a the given point, moved about the given centre-point by the given radius-change and angle-change'
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
    '''creates multiple copies of 'geometry' (a Point or list of steps including 
    Points). elements in a list that are not Points pass through and are replicated 
    without modification. each copy is moved about a centre point by the given 
    radius and angle (radians) relative to the radius and angle of each respective
    point in the previous copy of the geometry. return the moved geometry (original 
    geometry is not edited). 'quantity' includes the position of the original 
    geometry. return the new geometry as a list (original geometry is not edited). 
    '''
    steps_new = []
    for i in range(quantity):
        radius_now = radius*i
        angle_now = angle*i
        if type(geometry).__name__ == "Point":
            steps_new.append(move_geometry_polar(geometry, centre, radius_now, angle_now))
        else:
            steps_new.extend(move_geometry_polar(geometry, centre, radius_now, angle_now))
    return steps_new
