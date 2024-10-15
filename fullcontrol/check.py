from fullcontrol.extra_functions import flatten, first_point
from fullcontrol.common import Point
from typing import Union

def stop(message: str):
    from sys import exit
    print(f'---------------------------------------------------------\n   {message}\n---------------------------------------------------------')
    exit()

def check(steps: list):
    '''
    Check a list of steps and report what type of classes are included and whether the list is 2D.
    FullControl requires it to be 1D for processing.

    Parameters:
    - steps (list): A list of steps to be checked.

    Returns:
    - None

    Prints the check results, including the types of steps found in the list.
    '''
    if isinstance(steps, list):
        results = ""
        types = set(type(step).__name__ for step in steps)
        if "list" in types:
            results = "\n".join((
                "  warning - the list of steps must be a 1D list of fullcontrol class instances, it currently includes a 'list'",
                "  use fc.flatten() to convert it to 1D or check for accidental use of append() instead of extend()\n"
            ))
        results += f"  step types {types}"
    else:
        results = "  warning - the design must be a 1D list of fullcontrol class instances, it currently a single object, not a list"
    print("check results:\n" + results)


def fix(steps: list, result_type: str, controls):
    
    types = set(type(step).__name__ for step in steps)
    if "list" in types:
        print("warning - the list of steps should be a 1D list of fullcontrol class instances, it currently includes a 'list'\n   - fc.flatten() is being used to convert the design to a 1D list")
        steps = flatten(steps)

    point0 = first_point(steps, fully_defined=False)

    # if any of x y z are None, warn the user:      
    if any(val is None for val in (point0.x, point0.y, point0.z)):
        print(f"warning - the first point in the design should have all x y z values defined\n   - it is currently ({point0}) ... any x/y/z currently `None` will be set to 0 - fix this issue before printing")
        point0.x = point0.x or 0
        point0.y = point0.y or 0
        point0.z = point0.z or 0
    
    if result_type == 'plot' and controls.color_type == 'manual':
        if point0.color is None:
            stop(message = "error - for fc.PlotControls(color_type='manual') the first point in the design must have a color attribute defined")

    return steps

def check_points(geometry: Union[Point, list], check: str):
    
    if check == 'polar_xy':
        def check_point(point: Point):
            if point.x is None or point.y is None:
                raise Exception(f"polar transformations can only be applied to points with both x and y values. Attempted for point ({point})") 
        if isinstance(geometry, Point):
            check_point(geometry)
        else:
            for step in geometry:
                if isinstance(step, Point):
                    check_point(step)