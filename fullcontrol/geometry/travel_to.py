from fullcontrol.geometry import Point, Extruder


def travel_to(point: Point) -> list:
    '''Returns a list of objects to turn extrusion off, travel to a point, then turn extrusion on.

    Args:
        point (Point): The destination point to travel to.

    Returns:
        list: A list of objects representing the steps to perform the travel.

    Raises:
        Exception: If an object of a type other than Point is supplied.

    '''
    if type(point).__name__ != 'Point':
        raise Exception(f'an object of type "{type(point).__name__}" was supplied. a Point object must be supplied')
    return [Extruder(on=False), point, Extruder(on=True)]
