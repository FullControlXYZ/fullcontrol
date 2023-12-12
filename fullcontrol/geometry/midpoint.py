
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


def interpolated_point(point1: Point, point2: Point, interpolation_fraction: float) -> Point:
    'return an interpolated point a fraction of the way from point1 to point2'
    x_inter = point1.x+interpolation_fraction * \
        (point2.x-point1.x) if point1.x != None or point2.x != None else None
    y_inter = point1.y+interpolation_fraction * \
        (point2.y-point1.y) if point1.y != None or point2.y != None else None
    z_inter = point1.z+interpolation_fraction * \
        (point2.z-point1.z) if point1.z != None or point2.z != None else None
    return Point(x=x_inter, y=y_inter, z=z_inter)
