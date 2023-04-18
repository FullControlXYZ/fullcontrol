
from fullcontrol.common import *
from fullcontrol.geometry import *

# see http://www.ambrsoft.com/MathCalc/Line/TwoLinesIntersection/TwoLinesIntersection.htm

# def line_intersection_by_mc(m1: Point, c1: Point, m2: Point, c2: Point, ) -> Point:
#   'find the intersection point between two lines, defined by m1,c1 and m2,c2. return intersection Point with z=None'
#   # see http://www.ambrsoft.com/MathCalc/Line/TwoLinesIntersection/TwoLinesIntersection.htm
#   x_int = (c1-c2)/(m2-m1)
#   y_int = (c1*m2-c2*m1)/(m2-m1)
#   return Point(x=x_int,y=y_int)

# def find_mc(p1: Point, p2: Point) -> DotDict:
#   'return m and c for the equation of an XY line from p1 to p2. return dictionary of m and c (actually, a DotDict accessible by .m and .c)'
#   m = (p2.y-p1.y)/(p2.x-p1.x) # gradient of line
#   c = p1.y-m*p1.x # intercept of line
#   return DotDict({'m':m, 'c':c})

# def line_intersection_by_pointsmc(a1: Point, a2: Point, b1: Point, b2: Point, ) -> Point:
#   'find the intersection point between two lines, one defined by Points a1,a2, the other by b1,b2. return intersection Point with z value the same as Point a1'
#   # see http://www.ambrsoft.com/MathCalc/Line/TwoLinesIntersection/TwoLinesIntersection.htm
#   mc1 = find_mc(a1,a2)
#   mc2 = find_mc(b1,b2)
#   p_int = line_intersection_by_mc(mc1.m, mc1.c, mc2.m, mc2.c)
#   p_int.z = a1.z
#   return p_int


def line_intersection_by_points_XY(point_a1: Point, point_a2: Point, point_b1: Point, point_b2: Point) -> Point:
    '''find the intersection point between two lines, one defined by Points a1, a2, the other by 
    b1, b2. only x and y components are considered. return intersection Point with z value the same 
    as Point p1
    '''
    # see http://www.ambrsoft.com/MathCalc/Line/TwoLinesIntersection/TwoLinesIntersection.htm
    # see https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    # this approach works with lines in the x or y direction, whereas calculation using m and c may fail due to division by zero.
    x1, x2, x3, x4, y1, y2, y3, y4 = point_a1.x, point_a2.x, point_b1.x, point_b2.x, point_a1.y, point_a2.y, point_b1.y, point_b2.y
    try:
        # x_int = ((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1))/((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
        # y_int = ((x2*y1-x1*y2)*(y4-y3)+(x4*y3+x3*y4)*(y2-y1))/((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
        x_int = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)) / \
            ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        y_int = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)) / \
            ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        return Point(x=x_int, y=y_int, z=point_a1.z)
    except:
        raise Exception(
            f'error: no intercept found. are the lines parallel? or are points coincident? or similar?\na1={point_a1}\na2={point_a2}\nb1={point_b1}\nb2={point_b2}')


def line_intersection_by_polar_XY(point1: Point, angle1: float, point2: Point, angle2: float) -> Point:
    '''find the intersection point between two polar lines, defined by Points point1, angle1, and 
    point2, angle2. only x and y components are considered. return intersection Point with z value 
    the same as Point p1
    '''
    # see http://www.ambrsoft.com/MathCalc/Line/TwoLinesIntersection/TwoLinesIntersection.htm
    p_int = line_intersection_by_points_XY(point1, polar_to_point(point1, 1, angle1), point2, polar_to_point(point2, 1, angle2))
    p_int.z = point1.z
    return p_int


def crossing_lines_check_XY(point_a1: Point, point_a2: Point, point_b1: Point, point_b2: Point) -> bool:
    '''check if two lines cross within their length, one defined by Points a1,a2, the other by b1,b2. 
    only x and y components are considered. return true if they cross
    '''
    # see https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    # see https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    def ccw(A, B, C):
        return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
    return ccw(point_a1, point_b1, point_b2) != ccw(point_a2, point_b1, point_b2) and ccw(point_a1, point_a2, point_b1) != ccw(point_a1, point_a2, point_b2)
