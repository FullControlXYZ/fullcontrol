from fullcontrol import Point, relative_point


def setup_p():
    'return P function for concise definition of fc.Points'
    def P(x, y, z):
        return(Point(x=x, y=y, z=z))
    return(P)


def setup_r(steps):
    'return R function for concise definition of fc.Points relative to the last point in the supplied list'
    def R(x, y, z):
        return(relative_point(steps, x, y, z))
    return(R)
