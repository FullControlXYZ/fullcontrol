from fullcontrol.common import Point
from itertools import chain
from copy import deepcopy
from typing import Union


def points_only(steps: list, track_xyz: bool = True) -> list:
    '''Converts steps of Points and control to only Points and returns a new list.
    
    Args:
        steps (list): A list of steps containing Points and control data.
        track_xyz (bool, optional): Specifies whether to track the xyz values of the Points. 
            If True, the returned list will contain a tracked list of points with all xyz values defined. 
            If False, the Points are returned as they are defined, including attributes with value=None.
    
    Returns:
        list: A new list containing only Points.
    
    If track_xyz=False, Points are returned as they are defined, including attributes with value=None.
    If track_xyz=True, the returned list contains a tracked list of points with all xyz defined: 
    when some of xyz are not defined, they are calculated from the previous step. 
    The first point in the returned list will be the first point for which all xyz were defined/tracked.
    '''
    new_steps = []
    for step in steps:
        if isinstance(step, Point):  # only consider Point data
            new_steps.append(step)
    if track_xyz:
        for i in range(len(new_steps)-1):
            # fill in any None attributes for the next point with the most recent previous value:
            next_point = deepcopy(new_steps[i])
            # update values that are not None
            next_point.update_from(new_steps[i+1])
            new_steps[i+1] = next_point
        # delete initial elements prior to all of x y and z have values != None:
        loop = True
        while loop:
            if new_steps[0].x == None or new_steps[0].y == None or new_steps[0].z == None:
                del new_steps[0]
            else:
                loop = False
    return new_steps


def relative_point(reference: Union[Point, list], x_offset: float, y_offset: float, z_offset: float):
    '''
    Returns an fc.Point object with x, y, z positions relative to a reference point.
    
    Args:
        reference (Union[Point, list]): The reference point or a list of points. If a list is supplied, 
                                        the last point in the list is used as the reference point.
        x_offset (float): The offset in the x-axis.
        y_offset (float): The offset in the y-axis.
        z_offset (float): The offset in the z-axis.
    
    Returns:
        fc.Point: A new fc.Point object with the updated x, y, z positions.
    
    Raises:
        Exception: If the reference object is not a Point or a list containing at least one point.
        Exception: If the reference point does not have all of x, y, z attributes defined.
    '''
    pt = None
    if isinstance(reference, Point):
        pt = reference
    elif isinstance(reference, list):
        list_len = len(reference)
        for i in range(list_len):
            if isinstance(reference[-(i+1)], Point):
                pt = reference[-(i+1)]
                break
    if pt == None:
        raise Exception(f'The reference object must be a Point or a list containing at least one point')
    if None in [pt.x, pt.y, pt.z]:
        raise Exception(f'The reference point must have all of x, y, z attributes defined (x={pt.x}, y={pt.y}, z={pt.z})')
    new_pt = deepcopy(pt)
    new_pt.x, new_pt.y, new_pt.z = pt.x + x_offset, pt.y + y_offset, pt.z + z_offset
    return new_pt


def flatten(steps: list) -> list:
    '''
    Takes a list in which some elements are lists in the second dimension.
    Returns a flattened 1D list.

    Parameters:
        steps (list): The input list containing elements, some of which may be lists.

    Returns:
        list: A flattened 1D list.

    Example:
        >>> flatten([[1, 2], [3, 4], [5, 6]])
        [1, 2, 3, 4, 5, 6]
    '''
    return list(chain.from_iterable(step if isinstance(step, list) else [step]
                                    for step in steps))


def linspace(start: float, end: float, number_of_points: int) -> list:
    '''
    Generate evenly spaced floats from start to end.

    Args:
        start (float): The starting value of the range.
        end (float): The ending value of the range.
        number_of_points (int): The number of points to generate.

    Returns:
        list: A list of number_of_points floats, including the start and end values.
    '''
    return [start + float(x)/(number_of_points-1)*(end-start) for x in range(number_of_points)]


def first_point(steps: list, fully_defined: bool = True) -> Point:
    '''
    Return the first Point in the list.
    
    Parameters:
        - steps (list): A list of steps.
        - fully_defined (bool): If True, return the first Point with all x, y, z values defined.
    
    Returns:
        - Point: The first Point in the list.
    
    Raises:
        - Exception: If no point is found in steps with all x, y, z values defined and fully_defined is True.
        - Exception: If no point is found in steps and fully_defined is False.
    '''
    if isinstance(steps, list):
        for step in steps:
            if isinstance(step, Point):
                if fully_defined and any(val is None for val in (step.x, step.y, step.z)):
                    continue
                return step
    if fully_defined:
        raise Exception('No point found in steps with all of x y z defined')
    if not fully_defined:
        raise Exception('No point found in steps')
    
def last_point(steps: list, fully_defined: bool = True) -> Point:
    '''
    Return the last Point in the list.
    
    Parameters:
        - steps (list): A list of steps.
        - fully_defined (bool): If True, return the last Point with all x, y, z values defined.
    
    Returns:
        - Point: The last Point in the list.
    
    Raises:
        - Exception: If no point is found in steps with all x, y, z values defined and fully_defined is True.
        - Exception: If no point is found in steps and fully_defined is False.
    '''
    return first_point(list(reversed(steps)), fully_defined)


def export_design(steps: list, filename: str):
    '''
    Export design (list of steps) to a JSON file.

    Parameters:
        steps (list): List of steps representing the design.
        filename (str): Name of the output JSON file.

    Returns:
        None
    '''
    import json
    with open(filename + '.json', 'w', encoding='utf-8') as f:
        json.dump(steps, f, ensure_ascii=False, indent=4, default=lambda x: {'type': type(x).__name__, 'data': x.__dict__})


def import_design(fc_module_handle, filename: str):
    '''
    Import a previously exported design (list of steps).

    Args:
        fc_module_handle: The fc module that was imported to create the design originally (typically fc in documentation).
        filename: The name of the file to import the design from (without the .json extension).

    Returns:
        A list of steps representing the imported design.
    '''
    import json
    with open(filename + '.json') as f:
        data = json.load(f)
    steps = []
    for step in data:
        class_ = getattr(fc_module_handle, step['type'])
        step = class_.parse_obj(step['data'])
        steps.append(step)
    return steps
