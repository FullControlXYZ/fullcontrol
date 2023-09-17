from fullcontrol.geometry import Point, Vector

def intersectXY(point1: Point, point2: Point, point3: Point, point4: Point) -> Point:
    """returns intersect point of two lines, one going through point1 and point2, the second through point3 and point4.
       return new Point with z = point1.z
    """
    try:
        point_x = ( (point1.x*point2.y - point1.y*point2.x)*(point3.x - point4.x) - (point1.x - point2.x)*(point3.x*point4.y - point3.y*point4.x) )/( (point1.x - point2.x)*(point3.y - point4.y) - (point1.y - point2.y)*(point3.x - point4.x) )
        point_y = ( (point1.x*point2.y - point1.y*point2.x)*(point3.y - point4.y) - (point1.y - point2.y)*(point3.x*point4.y - point3.y*point4.x) )/( (point1.x - point2.x)*(point3.y - point4.y) - (point1.y - point2.y)*(point3.x - point4.x) )
        return Point(x=point_x, y=point_y, z=point1.z)
    except ZeroDivisionError:
        print("Error: no intersect point, provided lines are parallel or coincident")
    

def intersectXY_from_vector(point1: Point, vector1: Vector, point2: Point, vector2: Vector) -> Point:
    """returns intersect point of two lines, one starting at point1 with direction vector1, the second starting at point2 with direction vector2
       return new Point with z = point1.z
    """
    try:
        return intersectXY(point1=point1, point2=Point(x=vector1.x+point1.x, y=vector1.y+point1.y, z=point1.z),
                           point3=point2, point4=Point(x=vector2.x+point2.x, y=vector2.y+point2.y, z=point1.z))
    except ZeroDivisionError:
        print("Error: no intersect point, provided lines are parallel or coincident")
    except:
        print("Error")