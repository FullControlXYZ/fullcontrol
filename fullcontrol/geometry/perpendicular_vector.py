from fullcontrol.geometry import Point, Vector

def perpendicular_vectorXY(start_point: Point, end_point: Point) -> Vector:
    'returns perpendicular 2d-vector from a line through two points, according to the right-hand rule'

    return Vector(x=-(point2.y-point1.y), y=point2.x-point1.x)

def perpendicular_vectorXY_from_vector(vector: Vector) -> Vector:
    'returns perpendicular 2d-vector to a vector, according to the right-hand rule'
    
    return Vector(x=-vector.y, y=vector.x)
