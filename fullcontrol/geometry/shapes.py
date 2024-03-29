
from fullcontrol.geometry import Point, arcXY, variable_arcXY, elliptical_arcXY
from math import tau


def rectangleXY(start_point: Point, x_size: float, y_size: float, cw: bool = False) -> list:
    '''
    Generate a 2D XY rectangle starting from a given Point, with specified size.
    
    Args:
        start_point (Point): The starting point of the rectangle.
        x_size (float): The size of the rectangle in the X-axis.
        y_size (float): The size of the rectangle in the Y-axis.
        cw (bool, optional): Specifies the direction of the rectangle. 
            If True, the rectangle is generated in a clockwise direction. 
            If False (default), the rectangle is generated in a counter-clockwise direction.
    
    Returns:
        list: A list of five Points representing the rectangle. The list begins and ends with the same Point.
    '''
    point1 = Point(x=start_point.x+x_size*(not cw), y=start_point.y + y_size*cw, z=start_point.z)  # boolean False=0
    point2 = Point(x=start_point.x+x_size, y=start_point.y+y_size, z=start_point.z)
    point3 = Point(x=start_point.x+x_size*cw, y=start_point.y+y_size*(not cw), z=start_point.z)
    return [start_point.copy(), point1, point2, point3, start_point.copy()]


def circleXY(centre: Point, radius: float, start_angle: float, segments: int = 100, cw: bool = False) -> list:
    '''
    Generate a 2D-XY circle with the specified number of segments (defaulting to 100), centred about a Point,
    with the given radius, starting at the specified polar angle (in radians), and with the z-position the same as that
    of the centre Point.

    Parameters:
        centre (Point): The centre point of the circle.
        radius (float): The radius of the circle.
        start_angle (float): The starting angle (in radians) of the circle.
        segments (int, optional): The number of segments to divide the circle into (default is 100).
        cw (bool, optional): If True, the circle will be generated in clockwise direction (default is False).

    Returns:
        list: A list of Points representing the circle.

    '''
    return arcXY(centre, radius, start_angle, tau*(1-(2*cw)), segments)



def circleXY_3pt(pt1: Point, pt2: Point, pt3: Point, start_angle: float, segments: int = 100, cw: bool = False) -> list:
    '''Generate a 2D-XY circle with the specified number of segments (defaulting to 100), defined by three points
    that the circle passes through. The start point in the returned list of points is defined by a polar angle 
    (in radians). The z-position is the same as that of pt1. Returns a list of Points.
    
    Args:
        pt1 (Point): The first point that the circle passes through.
        pt2 (Point): The second point that the circle passes through.
        pt3 (Point): The third point that the circle passes through.
        start_angle (float): The polar angle (in radians) that defines the start point of the circle.
        segments (int, optional): The number of segments to divide the circle into (default is 100).
        cw (bool, optional): If True, generates the circle in clockwise direction (default is False).
    
    Returns:
        list: A list of Points representing the circle.
    
    Raises:
        Exception: If the three points are collinear, meaning no unique circle can be defined.
    '''
    D = 2 * (pt1.x * (pt2.y - pt3.y) + pt2.x * (pt3.y - pt1.y) + pt3.x * (pt1.y - pt2.y))
    if D == 0:
        raise Exception('The points are collinear, no unique circle')
    x_centre = ((pt1.x**2 + pt1.y**2) * (pt2.y - pt3.y) + (pt2.x**2 + pt2.y**2) * (pt3.y - pt1.y) + (pt3.x**2 + pt3.y**2) * (pt1.y - pt2.y)) / D
    y_centre = ((pt1.x**2 + pt1.y**2) * (pt3.x - pt2.x) + (pt2.x**2 + pt2.y**2) * (pt1.x - pt3.x) + (pt3.x**2 + pt3.y**2) * (pt2.x - pt1.x)) / D
    radius = ((pt1.x - x_centre)**2 + (pt1.y - y_centre)**2)**0.5
    centre = Point(x=x_centre, y=y_centre, z=pt1.z)
    return arcXY(centre, radius, start_angle, tau*(1-(2*cw)), segments)



def ellipseXY(centre: Point, a: float, b: float, start_angle: float, segments: int = 100, cw: bool = False) -> list:
    '''
    Generate a 2D-XY ellipse with the specified number of segments (defaulting to 100), centred about a Point,
    with the given width (a) and height (b), starting at the specified polar angle (in radians), and with the z-position
    the same as that of the centre Point. Returns a list of Points representing the ellipse.
    
    Parameters:
    - centre: The centre Point of the ellipse.
    - a: The width of the ellipse.
    - b: The height of the ellipse.
    - start_angle: The starting angle (in radians) for generating the ellipse.
    - segments: The number of segments to use for generating the ellipse (default is 100).
    - cw: A boolean indicating whether to generate the ellipse in clockwise direction (default is False).
    
    Returns:
    - A list of Points representing the generated ellipse.
    '''
    return elliptical_arcXY(centre, a, b, start_angle, tau*(1-(2*cw)), segments)



def polygonXY(centre: Point, enclosing_radius: float, start_angle: float, sides: int, cw: bool = False) -> list:
    '''
    Generate a 2D-XY polygon with the specified number of sides, centered about a Point, sized based on the enclosing radius,
    starting at the specified polar angle (in radians). The default direction is counter-clockwise.
    
    Parameters:
        - centre (Point): The center point of the polygon.
        - enclosing_radius (float): The radius of the circle that encloses the polygon.
        - start_angle (float): The starting angle (in radians) for generating the polygon.
        - sides (int): The number of sides of the polygon.
        - cw (bool, optional): If True, the polygon will be generated in clockwise direction. Default is False (counter-clockwise).
    
    Returns:
        - list: A list of Point objects representing the vertices of the polygon. The list will have one more Point than the number of sides,
                since it begins and ends with the same Point.
    '''
    return arcXY(centre, enclosing_radius, start_angle, tau*(1-(2*cw)), sides)  # cw parameter used to achieve +1 or -1




def spiralXY(centre: Point, start_radius: float, end_radius: float, start_angle: float, n_turns: float, segments: int, cw: bool = False) -> list:
    '''
    Generate a 2D-XY spiral with the specified number of segments and turns (partial turns permitted), centred about a Point.
    
    Parameters:
    - centre: The centre point of the spiral.
    - start_radius: The radius of the spiral at the starting point.
    - end_radius: The radius of the spiral at the ending point.
    - start_angle: The starting polar angle of the spiral in radians.
    - n_turns: The number of turns the spiral should make.
    - segments: The number of segments the spiral should be divided into.
    - cw: A boolean indicating whether the spiral should be generated in clockwise direction (default: False).
    
    Returns:
    - A list of Points representing the spiral. The list begins with the Point at the start of the first segment and ends at the Point at the end of the final segment.
    '''
    return variable_arcXY(centre, start_radius, start_angle, arc_angle=n_turns*tau*(1-(2*cw)), segments=segments, radius_change=end_radius-start_radius, z_change=0)


def helixZ(centre: Point, start_radius: float, end_radius: float, start_angle: float, n_turns: float, pitch_z: float, segments: int, cw: bool = False) -> list:
    '''
    Generate a helix in the Z direction with the specified number of segments and turns (partial turns permitted), centred about the Point centre, sized based on the start and end radius,
    starting at the specified polar angle (radians), defaulting to counter-clockwise. The returned list will begin with the Point at the start of the first segment 
    and end at the Point at the end of the final segment.

    Parameters:
    - centre: The centre Point of the helix.
    - start_radius: The starting radius of the helix.
    - end_radius: The ending radius of the helix.
    - start_angle: The starting polar angle (in radians) of the helix.
    - n_turns: The number of turns of the helix.
    - pitch_z: The pitch (vertical distance per turn) of the helix.
    - segments: The number of segments to divide the helix into.
    - cw: A boolean indicating whether the helix should be generated in a clockwise direction. Default is False (counter-clockwise).

    Returns:
    - A list of Points representing the helix, starting at the Point at the start of the first segment and ending at the Point at the end of the final segment.
    '''
    return variable_arcXY(centre, start_radius, start_angle, arc_angle=n_turns*tau*(1-(2*cw)), segments=segments, radius_change=end_radius-start_radius, z_change=pitch_z*n_turns)
