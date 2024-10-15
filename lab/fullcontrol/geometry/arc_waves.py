from fullcontrol.common import linspace
from fullcontrol import Point, polar_to_point
from math import tau, cos


def arc_sinewaveXY(centre: Point, radius: float, amplitude: float, start_angle: float, arc_angle: float, periods: int, segments_per_period: int = 16, extra_half_period: bool = False, phase_shift: float = 0) -> list:
    '''
    Generate a sine wave with the set number of periods, starting at the start_point, with 
    a given wave direction (polar angle in radians), given amplitude, with the distance between 
    the midpoint of each line of the sine wave set by line_spacing. Optionally, an extra half 
    period can be added and the wave can be phase-shifted.

    Parameters:
    - start_point (Point): The starting point of the sine wave.
    - radius (float): The radius of the arc followed by the sine wave.
    - amplitude (float): The radial amplitude of the sine wave.
    - start_angle (float): The starting polar angle (radians) of the arc of the sine wave.
    - arc_angle (float): The angle (radians) of the arc of the sine wave.
    - periods (float): The number of periods of the sine wave.
    - segments_per_period (int, optional): The number of segments to divide each period into (default is 16).
    - extra_half_period (bool, optional): Whether to add an extra half period to the wave (default is False) - this extra half sinewave occurs within the original 'arc_angle'.
    - phase_shift (float, optional): The phase shift of the sine wave (default is 0).

    Returns:
    - list: A list of Points representing the sine wave.
    '''
    period_angle = arc_angle/(periods + 0.5*extra_half_period)
    a_steps = linspace(start_angle, start_angle+arc_angle, int(segments_per_period*periods)+extra_half_period*int(0.5*segments_per_period)+1)
    r_steps = [radius + amplitude * (0.5-0.5*cos(((a % period_angle)/period_angle)*tau + phase_shift)) for a in a_steps]
    return [polar_to_point(centre, r_steps[i], a_steps[i])for i in range(len(a_steps))]
    
