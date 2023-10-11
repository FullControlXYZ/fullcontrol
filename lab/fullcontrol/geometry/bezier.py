from lab.fullcontrol.geometry import Point

# Bezier curve
# from https://orthallelous.wordpress.com/2020/06/21/pure-python-bezier-curve/
# Also consider https://towardsdatascience.com/b%C3%A9zier-curve-bfffdadea212 for concise 3D(+) bezier curves
# and https://codereview.stackexchange.com/questions/240710/pure-python-b%C3%A9zier-curve-implementation

try:
    # combinations are standard in python 3.8
    from math import comb
except ImportError:
    from math import factorial

    def comb(n, k):  # also nCr
        "k combinations of n"
        v, n1 = 1, n + 1
        nk = n1 - k
        for i in range(nk, n1):
            v *= i
        return v // factorial(k)

# keep previously computed nCr values
_ncr_precmp = {}  # for use in bernstein poly/bezier curves
# gives a slight speed increase for a large number of points along a bezier


def bernstein(n, i, x):
    "bernstein polynomial n, i at point x; b_i,n(x)"
    p = _ncr_precmp.get((n, i))
    if p is None:
        p = comb(n, i)
        _ncr_precmp[(n, i)] = p
    return p * x ** i * (1 - x) ** (n - i)


def bezier_original(clpts, numpts=10, endpt=True):
    'returns numpts positions of a bezier curve controlled by clpts, ending on the final control point if endpt=True'
    if not all(map(lambda x: len(x) == len(clpts[0]), clpts)):
        err = ValueError("control points are different dimensions")
        raise err
    if len(clpts) < 2:
        err = ValueError("at least two control points are required")
        raise err

    n, xy = len(clpts), []
    step = float(numpts - 1 if endpt else numpts)
    # control points collected by their dimensions
    dims = list(zip(*clpts))
    # [(all x value dimensions), (all y value dimensions), etc...]

    for t in range(numpts):
        # collect bernstein values for each control point
        bv = [bernstein(n - 1, v, t / step) for v in range(n)]

        # summation along dimension values and bernstein values
        pt = []
        for d in dims:
            pt.append(sum(i * j for i, j in zip(d, bv)))
        xy.append(tuple(pt))
    return xy


def bezier(control_points, num_points=10, end_point=True):
    'returns a bezier curve with num_points based on the supplied control points, ending on the final control point if end_point is True. returns list of points in curve'
    clpts = [[point.x, point.y, point.z] for point in control_points]
    bez_curve = bezier_original(clpts, num_points, end_point)
    return [Point(x=bez_curve[i][0], y=bez_curve[i][1], z=bez_curve[i][2]) for i in range(len(bez_curve))]


def bezierXYdiscrete(control_points, num_points=10, end_point=True):
    'legacy function - use bezier() instead'
    return bezier(control_points, num_points, end_point)


def refine_bezier_points(control_points, segments_between_control_points=10, iteration_fraction=0.5, iterations=20):
    '''iteratively move bezier control points until the bezier curve directly passes through each control point.
    iteration fraction indicates how far to move the control points in each iteration, relative to the distance
    between the nearest point of the bezier curve to the control point. return list of new control points'''

    from copy import deepcopy

    def calculate_bezier(t, ctrl_points):
        n = len(ctrl_points) - 1
        result = Point(x=0, y=0, z=0)
        for i in range(n + 1):
            binomial = binomial_coefficient(n, i)
            result = add_points(result, scale_point(binomial * (1 - t) ** (n - i) * t ** i, ctrl_points[i]))
        return result

    def binomial_coefficient(n, k):
        if 0 <= k <= n:
            result = 1
            for i in range(1, min(k, n - k) + 1):
                result = result * (n - i + 1) // i
            return result
        else:
            return 0

    def subtract_points(point1, point2):
        return Point(x=point1.x - point2.x, y=point1.y - point2.y, z=point1.z - point2.z)

    def add_points(point1, point2):
        return Point(x=point1.x + point2.x, y=point1.y + point2.y, z=point1.z + point2.z)

    def scale_point(scalar, point):
        return Point(x=scalar * point.x, y=scalar * point.y, z=scalar * point.z)

    def magnitude(point):
        return (point.x ** 2 + point.y ** 2 + point.z ** 2) ** 0.5

    num_points = (segments_between_control_points * (len(control_points)-1))+1
    adjusted_control_points = deepcopy(control_points)
    for _ in range(iterations):
        curve_points = []
        for t in [i / num_points for i in range(num_points + 1)]:
            curve_points.append(calculate_bezier(t, adjusted_control_points))

        for i, original_point in enumerate(control_points):
            closest_point = min(curve_points, key=lambda p: magnitude(subtract_points(p, original_point)))
            distance = magnitude(subtract_points(closest_point, original_point))

            # Check for zero distance to avoid division by zero
            if distance == 0:
                pass
            else:
                move_distance = iteration_fraction * distance
                direction = scale_point(1 / distance, subtract_points(original_point, closest_point))  # Reverse direction
                adjusted_control_points[i] = add_points(adjusted_control_points[i], scale_point(move_distance, direction))

    return adjusted_control_points


def bezier_through_points(control_points, num_points=10, iteration_fraction=0.5, iterations=20):
    '''create a bezier curve that approximately passes through the control points. control points are iteratively
    moved to get the bezier curve to pass closer to each control point with each iteration. iteration fraction
    indicates how far to move the control points in each iteration, relative to the distance between the nearest 
    point of the bezier curve to the control point.  
    '''
    num_segments = len(control_points) - 1
    segments_per_control_point_for_fitting = max(2, int(num_points/num_segments))
    return bezier(refine_bezier_points(control_points, segments_per_control_point_for_fitting, iteration_fraction, iterations), num_points)
