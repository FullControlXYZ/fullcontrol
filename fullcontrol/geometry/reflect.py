
from fullcontrol.geometry import Point


def reflectXY_mc(p: Point, m_reflect: float, c_reflect: float) -> Point:
    '''
    Reflects the x and y values of a Point about a line defined by m and c.
    
    Parameters:
        p (Point): The original Point to be reflected.
        m_reflect (float): The slope of the reflection line.
        c_reflect (float): The y-intercept of the reflection line.
    
    Returns:
        Point: A new Point with the x and y values reflected about the line, and the original z value.
    '''
    m_reflect_normal = -1 / m_reflect  # gradient of the normal of the reflection line
    # intercept of the normal of the reflection line
    c_reflect_normal = p.y - (m_reflect_normal * p.x)
    p_foot = Point(x=(c_reflect_normal - c_reflect) / (m_reflect - m_reflect_normal),  # See my onenote note (AG) - p_foot is the 'foot' of the original point on the reflection line
                   y=(c_reflect_normal - ((m_reflect_normal / m_reflect) * c_reflect)) / (1 - (m_reflect_normal / m_reflect)))
    return Point(x=p.x + 2 * (p_foot.x - p.x), y=p.y + 2 * (p_foot.y - p.y), z=p.z)


def reflectXY(p: Point, p1_reflect: Point, p2_reflect: Point) -> Point:
    '''
    Reflects the x and y values of a Point about a line defined by two Points.
    
    Parameters:
        p (Point): The Point to be reflected.
        p1_reflect (Point): The first Point defining the reflection line.
        p2_reflect (Point): The second Point defining the reflection line.
    
    Returns:
        Point: A new Point with the original z value and the reflected x and y values.
    '''
    # the if and elif avoid numerical errors associated with calculating the gradient of a vertical line
    if p2_reflect.x - p1_reflect.x == 0:  # reflection line in Y direction
        return Point(x=p.x + 2 * (p1_reflect.x - p.x), y=p.y, z=p.z)
    elif p2_reflect.y - p1_reflect.y == 0:  # reflection line in X direction
        return Point(x=p.x, y=p.y + 2 * (p1_reflect.y - p.y), z=p.z)
    else:
        # gradient of reflection line
        m_reflect = (p2_reflect.y - p1_reflect.y) / \
            (p2_reflect.x - p1_reflect.x)
        # intercept of reflection line
        c_reflect = p1_reflect.y - (m_reflect * p1_reflect.x)
        return reflectXY_mc(p, m_reflect, c_reflect)
