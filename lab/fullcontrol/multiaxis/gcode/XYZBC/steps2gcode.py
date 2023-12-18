
import os
from lab.fullcontrol.multiaxis.gcode.XYZBC.state import State
from lab.fullcontrol.multiaxis.gcode.XYZBC.controls import GcodeControls
from datetime import datetime


def gcode(steps: list, gcode_controls: GcodeControls = GcodeControls()):
    'return a gcode string generated from a list of steps'
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
        filename = gcode_controls.save_as + datetime.now().strftime("__%d-%m-%Y__%H-%M-%S.gcode")
        open(filename, 'w').write(gc)
    else:
        return gc
