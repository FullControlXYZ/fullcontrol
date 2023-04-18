from fullcontrol.geometry import Point, Extruder


def travel_to(point: Point) -> list:
    ''' returns a list of objects to turn extrusion off, travel to a point, then turn extrusion on
    '''
    if type(point).__name__ != 'Point':
        raise Exception(f'an object of type "{type(point).__name__}" was supplied. a Point object must be supplied')
    return [Extruder(on=False),point,Extruder(on=True)]
