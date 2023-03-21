from fullcontrol.geometry import Point, Extruder


def travel_to(point: Point) -> list:
    ''' returns a list of objects to turn extrusion off, travel to a point, then turn extrusion on
    '''
    return [Extruder(on=False),point,Extruder(on=True)]
