from typing import Union

from fullcontrol import *
import fullcontrol.geometry as xyz_geom
# base fc namespace for user access; infinaxis replacements override matching names
from lab.fullcontrol.infinaxis.axis import Axis
from lab.fullcontrol.infinaxis.controls import GcodeControls
from lab.fullcontrol.infinaxis.point import Point, configure_point
from lab.fullcontrol.infinaxis.printer import Printer
from lab.fullcontrol.infinaxis.steps2gcode import gcode
from lab.fullcontrol.infinaxis.xyz_add_axes import xyz_add_axes


def transform(steps: list, result_type: str, controls: Union[GcodeControls, PlotControls] = None, show_tips: bool = True):
    '''transform a fullcontrol design (a list of function class instances) into result_type
    "gcode" or "plot". Optionally, GcodeControls or PlotControls can be passed to control 
    how the gcode or plot are generated.
    '''

    if result_type == 'gcode':
        if controls is None: controls = GcodeControls()
        return gcode(steps, controls)

    elif result_type == 'plot':
        from fullcontrol.visualize.steps2visualization import visualize
        if controls is None: controls = PlotControls()
        return visualize(steps, controls, show_tips)
    
    else:
        raise ValueError(f"result_type '{result_type}' not recognized. Please use 'gcode' or 'plot' of fc.transform()")
