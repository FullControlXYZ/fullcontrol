from fullcontrol.geometry import Point, Extruder
from typing import Union
from fullcontrol.common import first_point

def travel_to(geometry: Union[Point, list]) -> list:
    '''Returns a list of objects to turn extrusion off, travel to a point, then turn extrusion on.

    Args:
        geometry (Point or List): The destination point to travel to or the list of points to which the first point in the list will be travelled to.

    Returns:
        list: A list of objects representing the steps to perform the travel.

    Raises:
        Exception: If an object of a type other than Point is supplied.

    '''
    if isinstance(geometry, Point):
        point = geometry
    elif isinstance(geometry, list):
        point = first_point(geometry)
    else:
        raise Exception(f'an object of type "{type(point).__name__}" was supplied. a Point object or list of points must be supplied')
    return [Extruder(on=False), point, Extruder(on=True)]
