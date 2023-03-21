
from fullcontrol.common import linspace
from fullcontrol.geometry import Point, Vector, move, move_polar


def ramp_xyz(steplist: list, x_change: float = 0, y_change: float = 0, z_change: float = 0) -> list:
    'linearly increase x/y/z values of a list of Points by x_change/y_change/z_change. return list of Points'
    x_steps = linspace(0, x_change, len(steplist))
    y_steps = linspace(0, y_change, len(steplist))
    z_steps = linspace(0, z_change, len(steplist))
    # for i in range(len(steplist)): steplist[i].z += z_steps[i]
    for i in range(len(steplist)):
        steplist[i] = move(steplist[i], Vector(x=x_steps[i], y=y_steps[i], z=z_steps[i]))
    return steplist


def ramp_polar(steplist: list, centre: Point, radius_change: float = 0, angle_change: float = 0) -> list:
    'linearly change angle and radius of a list of Points about point centre. return list of Points'
    r_steps = linspace(0, radius_change, len(steplist))
    a_steps = linspace(0, angle_change, len(steplist))
    for i in range(len(steplist)):
        steplist[i] = move_polar(steplist[i], centre, r_steps[i], a_steps[i])
    return steplist
