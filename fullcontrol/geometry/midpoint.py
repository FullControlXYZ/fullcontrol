
from fullcontrol.geometry import Point


def midpoint(point1: Point, point2: Point) -> Point:
    'return mid-point between two points'
    if point1.x != None and point2.x != None:
        mid_x = (point1.x + point2.x) / 2
    if point1.y != None and point2.y != None:
        mid_y = (point1.y + point2.y) / 2
    if point1.z != None and point2.z != None:
        mid_z = (point1.z + point2.z) / 2
    return Point(x=mid_x, y=mid_y, z=mid_z)
