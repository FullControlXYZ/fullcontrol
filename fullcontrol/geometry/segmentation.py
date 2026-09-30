
from fullcontrol.geometry import Point, interpolated_point, distance
from fullcontrol.common import linspace
from typing import Sequence, List

def segmented_line(point1: Point, point2: Point, segments: int) -> list:
    '''
    Return a list of Points linearly spaced between the start Point and end Point.
    The total number of Points in the list is segments+1.
    
    Parameters:
        point1 (Point): The start Point of the line segment.
        point2 (Point): The end Point of the line segment.
        segments (int): The number of segments to divide the line into.
    
    Returns:
        list: A list of Points linearly spaced between the start and end Points.
    '''
    x_steps = linspace(point1.x, point2.x, segments+1)
    y_steps = linspace(point1.y, point2.y, segments+1)
    z_steps = linspace(point1.z, point2.z, segments+1)
    return [Point(x=x_steps[i], y=y_steps[i], z=z_steps[i]) for i in range(segments+1)]

def segmented_line_from_fractions(point1: Point, point2: Point, fractions: Sequence[float]) -> List[Point]:
    """
    Return Points along the line from point1 to point2 with user-defined split locations.

    fractions:
        Strictly increasing values in (0, 1) giving internal split positions along the line.
        Endpoints are always included.
        Returns len(fractions) + 2 Points.
    """
    fr = [float(f) for f in fractions]
    if any(f <= 0.0 or f >= 1.0 for f in fr):
        raise ValueError("All fractions must be strictly between 0 and 1.")
    if any(fr[i] >= fr[i + 1] for i in range(len(fr) - 1)):
        raise ValueError("fractions must be strictly increasing.")

    dx = point2.x - point1.x
    dy = point2.y - point1.y
    dz = point2.z - point1.z

    t_values = [0.0] + fr + [1.0]
    return [
        Point(
            x=point1.x + t * dx,
            y=point1.y + t * dy,
            z=point1.z + t * dz,
        )
        for t in t_values
    ]


def segmented_line_from_lengths(point1: Point, point2: Point, lengths: Sequence[float]) -> List[Point]:
    """
    Return Points along the line from point1 to point2 with uneven spacing defined by segment weights.

    lengths:
        Positive numbers, one per segment. These are treated as relative weights and are normalised by their sum.
        They do NOT need to match the geometric distance between point1 and point2.
        Returns len(lengths) + 1 Points.
    """
    ls = [float(L) for L in lengths]
    if len(ls) < 1:
        raise ValueError("lengths must not be empty.")
    if any(L <= 0.0 for L in ls):
        raise ValueError("All values in lengths must be > 0.")
    total = float(sum(ls))
    if total <= 0.0:
        raise ValueError("sum(lengths) must be > 0.")

    dx = point2.x - point1.x
    dy = point2.y - point1.y
    dz = point2.z - point1.z

    t_values = [0.0]
    cum = 0.0
    for L in ls[:-1]:
        cum += L
        t_values.append(cum / total)
    t_values.append(1.0)

    return [
        Point(
            x=point1.x + t * dx,
            y=point1.y + t * dy,
            z=point1.z + t * dz,
        )
        for t in t_values
    ]




def segmented_path(points: list, segments: int) -> int:
    """
    Calculate a segmented path (equidistant points) based on a list of points and the desired number of segments.

    Args:
        points (list): A list of equidistant points along the path.
        segments (int): The desired number of segments.

    Returns:
        list: A list of points representing the segmented path.

    """
    lengths = [distance(points[i], points[i+1])
               for i in range(len(points)-1)]
    cumulative_length = [0]
    for length in lengths:
        cumulative_length.append(cumulative_length[-1]+length)
    seg_length = cumulative_length[-1]/segments
    path_pts = [points[0]]
    path_length_now = 0
    path_section_now = 0
    for seg in range(segments-1):
        path_length_now += seg_length
        while path_length_now > cumulative_length[path_section_now]:
            path_section_now += 1
        interpolation_length = path_length_now - \
            cumulative_length[path_section_now-1]
        interpolation_fraction = interpolation_length / \
            distance(points[path_section_now-1], points[path_section_now])
        path_pts.append(interpolated_point(
            points[path_section_now-1], points[path_section_now], interpolation_fraction))
    path_pts.append(points[-1])
    return path_pts
