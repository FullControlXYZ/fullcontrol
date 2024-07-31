
import os
from fullcontrol.gcode.point import Point
from fullcontrol.gcode.printer import Printer
from fullcontrol.gcode.extrusion_classes import ExtrusionGeometry, Extruder
from fullcontrol.gcode.state import State
from fullcontrol.gcode.controls import GcodeControls
from datetime import datetime
from fullcontrol.gcode.tips import tips


def gcode(steps: list, gcode_controls: GcodeControls, show_tips: bool):
    '''
    Generate a gcode string from a list of steps.

    Args:
        steps (list): A list of step objects.
        gcode_controls (GcodeControls, optional): An instance of GcodeControls class. Defaults to GcodeControls().

    Returns:
        str: The generated gcode string.
    '''
    gcode_controls.initialize()
    if show_tips: tips(gcode_controls)

    state = State(steps, gcode_controls)
    # need a while loop because some classes may change the length of state.steps
    while state.i < len(state.steps):
        # call the gcode function of each class instance in 'steps'
        gcode_line = state.steps[state.i].gcode(state)
        if gcode_line != None:
            state.gcode.append(gcode_line)
        state.i += 1
    gc = '\n'.join(state.gcode)

    if gcode_controls.save_as != None:
        filename = gcode_controls.save_as
        filename += datetime.now().strftime("__%d-%m-%Y__%H-%M-%S.gcode") if gcode_controls.include_date == True else '.gcode'
        open(filename, 'w').write(gc)

    return gc
