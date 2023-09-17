from fullcontrol.geometry import Point, Vector

def perpendicular_vectorXY(point1: Point, point2: Point) -> Vector:
    'returns perpendicular 2d-vector from a line'

    return Vector(x=-(point2.y-point1.y), y=point2.x-point1.x)

def perpendicular_vectorXY_from_vector(vector: Vector) -> Vector:
    'returns perpendicular 2d-vector to a vector'
    
    return Vector(x=-vector.y, y=vector.x)
