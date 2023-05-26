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
