
from fullcontrol.common import linspace
from fullcontrol.geometry import Point, Vector, move, move_polar


def ramp_xyz(steplist: list, x_change: float = 0, y_change: float = 0, z_change: float = 0) -> list:
    '''
    Linearly increase x/y/z values of a list of Points by x_change/y_change/z_change.
    
    Args:
        steplist (list): List of Points to be modified.
        x_change (float): Amount to increase x value of each Point. Default is 0.
        y_change (float): Amount to increase y value of each Point. Default is 0.
        z_change (float): Amount to increase z value of each Point. Default is 0.
    
    Returns:
        list: List of Points with modified x/y/z values.
    '''
    x_steps = linspace(0, x_change, len(steplist))
    y_steps = linspace(0, y_change, len(steplist))
    z_steps = linspace(0, z_change, len(steplist))
    # for i in range(len(steplist)): steplist[i].z += z_steps[i]
    for i in range(len(steplist)):
        steplist[i] = move(steplist[i], Vector(x=x_steps[i], y=y_steps[i], z=z_steps[i]))
    return steplist


def ramp_polar(steplist: list, centre: Point, radius_change: float = 0, angle_change: float = 0) -> list:
    '''
    Linearly changes the angle (radians) and radius of a list of Points about a given centre point.
    
    Args:
        steplist (list): A list of Points to be modified.
        centre (Point): The centre point about which the Points are modified.
        radius_change (float, optional): The amount by which to change the radius of each Point. Defaults to 0.
        angle_change (float, optional): The amount by which to change the angle (radians) of each Point. Defaults to 0.
    
    Returns:
        list: A list of modified Points.
    '''
    r_steps = linspace(0, radius_change, len(steplist))
    a_steps = linspace(0, angle_change, len(steplist))
    for i in range(len(steplist)):
        steplist[i] = move_polar(steplist[i], centre, r_steps[i], a_steps[i])
    return steplist
