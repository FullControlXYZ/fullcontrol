
from fullcontrol.geometry import Point
from fullcontrol.common import linspace


def segmented_line(point1: Point, point2: Point, segments: int) -> list:
    'return a list of Points linearly spaced between the start Point and end Point. a total of Points in list = segments+1'
    x_steps = linspace(point1.x, point2.x, segments+1)
    y_steps = linspace(point1.y, point2.y, segments+1)
    z_steps = linspace(point1.z, point2.z, segments+1)
    return [Point(x=x_steps[i], y=y_steps[i], z=z_steps[i]) for i in range(segments+1)]
