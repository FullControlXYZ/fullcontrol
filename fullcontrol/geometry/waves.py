
from fullcontrol.geometry import Point, Vector, point_to_polar, polar_to_point, move, move_polar
from math import pi, atan2


def squarewaveXYpolar(start_point: Point, direction_polar: float, amplitude: float, line_spacing: float, periods: int, extra_half_period: bool = False, extra_end_line: bool = False) -> list:
    ''''generate a squarewave with the set number of periods, starting at the start_point, with 
    a given wave direction (polar angle in radians), given amplitude, with the distance between 
    each line of the squarewave set by line_spacing. Optionally, an extra half period and/or one 
    extra line (top/bottom of squrewave) can be added. return list of Points
    '''
    steps = []
    steps.append(start_point.copy())
    for i in range(periods):
        steps.append(polar_to_point(centre=steps[-1], radius=amplitude, angle=direction_polar + pi/2))
        steps.append(polar_to_point(centre=steps[-1], radius=line_spacing, angle=direction_polar))
        steps.append(polar_to_point(centre=steps[-1], radius=amplitude, angle=direction_polar - pi/2))
        if i != periods - 1:
            steps.append(polar_to_point(centre=steps[-1], radius=line_spacing, angle=direction_polar))
    if extra_half_period:
        steps.append(polar_to_point(centre=steps[-1], radius=line_spacing, angle=direction_polar))
        steps.append(polar_to_point(centre=steps[-1], radius=amplitude, angle=direction_polar + pi/2))
    if extra_end_line:
        steps.append(polar_to_point(centre=steps[-1], radius=line_spacing, angle=direction_polar))
    return steps


def squarewaveXY(start_point: Point, direction_vector: Vector, amplitude: float, line_spacing: float, periods: int, extra_half_period: bool = False, extra_end_line: bool = False) -> list:
    ''''generate a square wave with the set number of periods, starting at the start_point, with 
    a given wave direction (dictated by xy components of a Vector), given amplitude, with the 
    distance between each line of the square wave set by line_spacing. Optionally, an extra half 
    period and/or one extra line (top/bottom of squrewave) can be added. return list of Points
    '''
    if direction_vector.x == None:
        direction_vector.x = 0
    if direction_vector.y == None:
        direction_vector.y = 0
    direction_polar = atan2(direction_vector.y, direction_vector.x)
    return squarewaveXYpolar(start_point, direction_polar, amplitude, line_spacing, periods, extra_half_period=extra_half_period, extra_end_line=extra_end_line)


def trianglewaveXYpolar(start_point: Point, direction_polar: float, amplitude: float, tip_separation: float, periods: int, extra_half_period: bool = False) -> list:
    ''''generate a triangle wave with the set number of periods, starting at the start_point, with 
    a given wave direction (polar angle in radians), given amplitude, with the distance between 
    neighbouring tips of the wave set by tip_separation. Optionally, an extra half period can be 
    added. return list of Points
    '''
    steps = []
    steps.append(start_point.copy())
    for i in range(periods):
        point_temp = polar_to_point(centre=steps[-1], radius=amplitude, angle=direction_polar + pi/2)
        steps.append(polar_to_point(centre=point_temp, radius=tip_separation/2, angle=direction_polar))
        point_temp = polar_to_point(centre=steps[-1], radius=amplitude, angle=direction_polar - pi/2)
        steps.append(polar_to_point(centre=point_temp, radius=tip_separation/2, angle=direction_polar))
    if extra_half_period:
        point_temp = polar_to_point(centre=steps[-1], radius=amplitude, angle=direction_polar + pi/2)
        steps.append(polar_to_point(centre=point_temp, radius=tip_separation/2, angle=direction_polar))
    return steps


def sinewaveXYpolar(start_point: Point, direction_polar: float, amplitude: float, period_length: float, periods: int, segments_per_period: int = 16, extra_half_period: bool = False, phase_shift: float = 0) -> list:
    '''generate a sine wave with the set number of periods, starting at the start_point, with 
    a given wave direction (polar angle in radians), given amplitude, with the distance between 
    the midpoint of each line of the sine wave set by line_spacing. Optionally, an extra half 
    period can be added and the wave can be phase-shifted. return list of Points
    '''
    from math import tau, cos
    steps = []
    for i in range(periods*segments_per_period + extra_half_period*int(0.5*segments_per_period) + 1):
        axis_distance_now = i * period_length / segments_per_period
        amplitude_now = amplitude * (0.5 - (0.5 * cos(((i / segments_per_period) * tau) + phase_shift)))
        steps.append(move(start_point, Vector(x=axis_distance_now, y=amplitude_now, z=0)))
    steps = move_polar(steps, start_point, 0, direction_polar)
    return steps
