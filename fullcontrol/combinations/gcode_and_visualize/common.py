
from typing import Union

# see comment in __init__.py about why this module exists

# import functions and classes that will be accessible to the user
from .classes import *
from fullcontrol.common import fix
from fullcontrol.common import check, flatten, linspace, export_design, import_design, points_only, relative_point, first_point, last_point
from fullcontrol.geometry import *
from fullcontrol.visualize.bounding_box import BoundingBox


def transform(steps: list, result_type: str, controls: Union[GcodeControls, PlotControls] = None, show_tips: bool = True):
    '''
    Transform a fullcontrol design (a list of class instances) into the specified result_type.
    
    Parameters:
        - steps (list): A list of function class instances representing the fullcontrol design.
        - result_type (str): The desired result type. Valid options are "gcode" or "plot".
        - controls (Union[GcodeControls, PlotControls], optional): Controls to customize the generation of gcode or plot. Defaults to None.
    
    Returns:
        - The transformed result based on the specified result_type.
    
    Raises:
        - None
    
    Example usage:
        transform(steps, "gcode", controls)
    '''

    
    if result_type == 'gcode':
        from fullcontrol.gcode.steps2gcode import gcode
        if controls is None: controls = GcodeControls()
        steps = fix(steps, result_type, controls)
        return gcode(steps, controls, show_tips)

    elif result_type == 'plot':
        from fullcontrol.visualize.steps2visualization import visualize
        if controls is None: controls = PlotControls()
        steps = fix(steps, result_type, controls)
        return visualize(steps, controls, show_tips)
    
    else:
        raise ValueError(f"result_type '{result_type}' not recognized. Please use 'gcode' or 'plot' of fclab.transform()")
