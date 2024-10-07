
from typing import Union

# # see comment in __init__.py about why this module exists

# # import functions and classes that will be accessible to the user
from fullcontrol.common import check
from fullcontrol.geometry import move, move_polar, travel_to  # don't import all geometry functions since they are not designed for multiaxis Points
from fullcontrol.combinations.gcode_and_visualize.classes import *
from .classes import *  # over-write above imports
import fullcontrol.geometry as xyz_geom
from .xyz_add_bc import xyz_add_bc


def transform(steps: list, result_type: str, controls: Union[GcodeControls, PlotControls] = None, show_tips: bool = True):
    '''transform a fullcontrol design (a list of function class instances) into result_type
    "gcode" or "plot". Optionally, GcodeControls or PlotControls can be passed to control 
    how the gcode or plot are generated.
    '''

    if result_type == 'gcode':
        from lab.fullcontrol.multiaxis.gcode.XYZBC.steps2gcode import gcode
        if controls is None: controls = GcodeControls()
        return gcode(steps, controls)

    elif result_type == 'plot':
        from fullcontrol.visualize.steps2visualization import visualize
        if controls is None: controls = PlotControls()
        return visualize(steps, controls, show_tips)
