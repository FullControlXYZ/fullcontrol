
from typing import Union

# see comment in __init__.py about why this module exists

# import functions and classes that will be accessible to the user
from .classes import *
from fullcontrol.common import check, flatten, linspace, export_design, import_design, points_only, relative_point, first_point
from fullcontrol.geometry import *


def transform(steps: list, result_type: str, controls: Union[GcodeControls, PlotControls] = None):
    '''transform a fullcontrol design (a list of function class instances) into result_type
    "gcode" or "plot". Optionally, GcodeControls or PlotControls can be passed to control 
    how the gcode or plot are generated.
    '''

    if result_type == 'gcode':
        from fullcontrol.gcode.steps2gcode import gcode
        if controls != None:
            return gcode(steps, controls)
        else:
            return gcode(steps)

    elif result_type == 'plot':
        from fullcontrol.visualize.steps2visualization import visualize
        if controls != None:
            return visualize(steps, controls)
        else:
            return visualize(steps)
