
from fullcontrol.geometry import Point, Vector, point_to_polar, polar_to_point, move, move_polar
from math import pi, atan2


def squarewaveXYpolar(start_point: Point, direction_polar: float, amplitude: float, line_spacing: float, periods: int, extra_half_period: bool = False, extra_end_line: bool = False) -> list:
    '''Generate a squarewave with the set number of periods, starting at the start_point, with 
    a given wave direction (polar angle in radians), given amplitude, with the distance between 
    each line of the squarewave set by line_spacing. Optionally, an extra half period and/or one 
    extra line (top/bottom of squrewave) can be added. Return a list of Points.
    
    Parameters:
    - start_point (Point): The starting point of the squarewave.
    - direction_polar (float): The polar angle in radians that determines the direction of the wave.
    - amplitude (float): The amplitude of the wave.
    - line_spacing (float): The distance between each line of the squarewave.
    - periods (int): The number of periods in the squarewave.
    - extra_half_period (bool, optional): Whether to add an extra half period at the end of the squarewave. Default is False.
    - extra_end_line (bool, optional): Whether to add an extra line at the top/bottom of the squarewave. Default is False.
    
    Returns:
    - list of Points: The list of Points representing the squarewave.
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
    '''Generate a square wave with the set number of periods, starting at the start_point, with 
    a given wave direction (dictated by xy components of a Vector), given amplitude, with the 
    distance between each line of the square wave set by line_spacing. Optionally, an extra half 
    period and/or one extra line (top/bottom of square wave) can be added. Return a list of Points.
    
    Parameters:
    - start_point (Point): The starting point of the square wave.
    - direction_vector (Vector): The direction vector of the square wave.
    - amplitude (float): The amplitude of the square wave.
    - line_spacing (float): The distance between each line of the square wave.
    - periods (int): The number of periods in the square wave.
    - extra_half_period (bool, optional): Whether to add an extra half period to the square wave. Defaults to False.
    - extra_end_line (bool, optional): Whether to add an extra line (top/bottom of square wave). Defaults to False.
    
    Returns:
    - list: A list of Points representing the square wave.
    '''
    if direction_vector.x == None:
        direction_vector.x = 0
    if direction_vector.y == None:
        direction_vector.y = 0
    direction_polar = atan2(direction_vector.y, direction_vector.x)
    return squarewaveXYpolar(start_point, direction_polar, amplitude, line_spacing, periods, extra_half_period=extra_half_period, extra_end_line=extra_end_line)



def trianglewaveXYpolar(start_point: Point, direction_polar: float, amplitude: float, tip_separation: float, periods: int, extra_half_period: bool = False) -> list:
    '''Generate a triangle wave with the set number of periods, starting at the start_point, with 
    a given wave direction (polar angle in radians), given amplitude, with the distance between 
    neighbouring tips of the wave set by tip_separation. Optionally, an extra half period can be 
    added. Return a list of Points.
    
    Args:
        start_point (Point): The starting point of the triangle wave.
        direction_polar (float): The polar angle in radians that determines the direction of the wave.
        amplitude (float): The amplitude of the wave.
        tip_separation (float): The distance between neighboring tips of the wave.
        periods (int): The number of periods in the wave.
        extra_half_period (bool, optional): Whether to add an extra half period to the wave. Defaults to False.
    
    Returns:
        list: A list of Points representing the triangle wave.
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
    '''
    Generate a sine wave with the set number of periods, starting at the start_point, with 
    a given wave direction (polar angle in radians), given amplitude, with the distance between 
    the midpoint of each line of the sine wave set by line_spacing. Optionally, an extra half 
    period can be added and the wave can be phase-shifted.

    Parameters:
    - start_point (Point): The starting point of the sine wave.
    - direction_polar (float): The polar angle in radians that determines the direction of the wave.
    - amplitude (float): The amplitude of the wave.
    - period_length (float): The length of each period of the wave.
    - periods (int): The number of periods in the wave.
    - segments_per_period (int, optional): The number of line segments per period. Defaults to 16.
    - extra_half_period (bool, optional): Whether to add an extra half period to the wave. Defaults to False.
    - phase_shift (float, optional): The phase shift of the wave. Defaults to 0.

    Returns:
    - list: A list of Points representing the sine wave.
    '''
    from math import tau, cos
    steps = []
    for i in range(periods*segments_per_period + extra_half_period*int(0.5*segments_per_period) + 1):
        axis_distance_now = i * period_length / segments_per_period
        amplitude_now = amplitude * (0.5 - (0.5 * cos(((i / segments_per_period) * tau) + phase_shift)))
        steps.append(move(start_point, Vector(x=axis_distance_now, y=amplitude_now, z=0)))
    steps = move_polar(steps, start_point, 0, direction_polar)
    return steps




def rasterXY(min_x: float, max_x: float, min_y: float, max_y: float, stepover: float) -> list:
    '''Generate a serpentine raster toolpath in the XY plane between the given bounds.
    Returns a list of Points. Each pair of points defines one horizontal pass, and the
    direction alternates on each successive pass.

    Parameters:
    - min_x (float): Minimum x bound.
    - max_x (float): Maximum x bound.
    - min_y (float): Minimum y bound.
    - max_y (float): Maximum y bound.
    - stepover (float): Distance between adjacent raster lines.

    Returns:
    - list of Points: The list of Points representing the raster path.
    '''
    if stepover <= 0:
        raise ValueError("stepover must be greater than 0")
    if max_x < min_x:
        raise ValueError("max_x must be greater than or equal to min_x")
    if max_y < min_y:
        raise ValueError("max_y must be greater than or equal to min_y")

    points = []

    n_passes = ceil((max_y - min_y) / stepover) + 1

    for i in range(n_passes):
        y = min_y + i * stepover

        # force exact last line onto max_y
        if i == n_passes - 1:
            y = max_y

        if i % 2 == 0:
            points.append(Point(x=min_x, y=y))
            points.append(Point(x=max_x, y=y))
        else:
            points.append(Point(x=max_x, y=y))
            points.append(Point(x=min_x, y=y))

    return points
