
from fullcontrol.geometry import Point


def midpoint(point1: Point, point2: Point) -> Point:
    '''
    Return the mid-point between two points.

    Args:
        point1 (Point): The first point.
        point2 (Point): The second point.

    Returns:
        Point: The mid-point between the two points.
    '''
    if point1.x != None and point2.x != None:
        mid_x = (point1.x + point2.x) / 2
    if point1.y != None and point2.y != None:
        mid_y = (point1.y + point2.y) / 2
    if point1.z != None and point2.z != None:
        mid_z = (point1.z + point2.z) / 2
    return Point(x=mid_x, y=mid_y, z=mid_z)


def interpolated_point(point1: Point, point2: Point, interpolation_fraction: float) -> Point:
    '''
    Return an interpolated point a fraction of the way from point1 to point2.

    Args:
        point1 (Point): The starting point.
        point2 (Point): The ending point.
        interpolation_fraction (float): The fraction of the distance between point1 and point2.

    Returns:
        Point: The interpolated point.

    '''
    x_inter = point1.x+interpolation_fraction * \
        (point2.x-point1.x) if point1.x != None or point2.x != None else None
    y_inter = point1.y+interpolation_fraction * \
        (point2.y-point1.y) if point1.y != None or point2.y != None else None
    z_inter = point1.z+interpolation_fraction * \
        (point2.z-point1.z) if point1.z != None or point2.z != None else None
    return Point(x=x_inter, y=y_inter, z=z_inter)


def centreXY_3pt(pt1: Point, pt2: Point, pt3: Point) -> Point:
    '''
    Calculate the centre point of a circle passing through three points.
    
    Args:
        pt1 (Point): First point on the circle.
        pt2 (Point): Second point on the circle.
        pt3 (Point): Third point on the circle.
    
    Returns:
        Point: centre point.
    
    Raises:
        Exception: If the three points are collinear, meaning no unique circle can be defined.
    '''
    D = 2 * (pt1.x * (pt2.y - pt3.y) + pt2.x * (pt3.y - pt1.y) + pt3.x * (pt1.y - pt2.y))
    if D == 0:
        raise Exception('The points are collinear, no unique circle')
    
    x_centre = ((pt1.x**2 + pt1.y**2) * (pt2.y - pt3.y) + (pt2.x**2 + pt2.y**2) * (pt3.y - pt1.y) + (pt3.x**2 + pt3.y**2) * (pt1.y - pt2.y)) / D
    y_centre = ((pt1.x**2 + pt1.y**2) * (pt3.x - pt2.x) + (pt2.x**2 + pt2.y**2) * (pt1.x - pt3.x) + (pt3.x**2 + pt3.y**2) * (pt2.x - pt1.x)) / D
    
    centre = Point(x=x_centre, y=y_centre, z=pt1.z)
    
    return centre
