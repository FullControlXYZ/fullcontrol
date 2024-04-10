
from fullcontrol.geometry import Point, point_to_polar


def distance(point1: Point, point2: Point) -> float:
    '''
    Calculate the Euclidean distance between two points in 3D space.

    Parameters:
        point1 (Point): The first point.
        point2 (Point): The second point.

    Returns:
        float: The distance between the two points.
    '''
    return ((point1.x-point2.x)**2+(point1.y-point2.y)**2+(point1.z-point2.z)**2)**0.5


def distance_forgiving(point1: Point, point2: Point) -> float:
    '''
    Calculate the distance between two points, ignoring the x, y, or z components if they are not defined in both points.

    Parameters:
    point1 (Point): The first point.
    point2 (Point): The second point.

    Returns:
    float: The distance between the two points.
    '''
    dist_x = 0 if point1.x == None or point2.x == None else point1.x - point2.x
    dist_y = 0 if point1.y == None or point2.y == None else point1.y - point2.y
    dist_z = 0 if point1.z == None or point2.z == None else point1.z - point2.z
    return ((dist_x)**2+(dist_y)**2+(dist_z)**2)**0.5


def angleXY_between_3_points(start_point: Point, mid_point: Point, end_point: Point) -> float:
    '''
    Returns the angle from start_point to end_point, about mid_point.

    Parameters:
    start_point (Point): The starting point.
    mid_point (Point): The middle point.
    end_point (Point): The ending point.

    Returns:
    float: The angle in degrees.
    '''
    return(point_to_polar(end_point, mid_point).angle - point_to_polar(start_point, mid_point).angle)


def path_length(points: list) -> float:
    """
    Calculates the total length of a path defined by a list of points.

    Args:
        points (list): A list of points defining the path.

    Returns:
        float: The total length of the path.
    """
    return sum([distance(points[i], points[i+1]) for i in range(len(points)-1)])
