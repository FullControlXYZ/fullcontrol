from lab.fullcontrol.multiaxis.gcode.XYZC0B1.point import Point as FiveAxisPoint
from fullcontrol.combinations.gcode_and_visualize.classes import Point as ThreeAxisPoint
from lab.fullcontrol.multiaxis.gcode.XYZC0B1.printer import Printer as FiveAxisPrinter
from fullcontrol.combinations.gcode_and_visualize.classes import Printer as ThreeAxisPrinter
from lab.fullcontrol.multiaxis.gcode.XYZC0B1.controls import GcodeControls as FiveAxisGcodeControls
from fullcontrol.combinations.gcode_and_visualize.common import GcodeControls as ThreeAxisGcodeControls


class Point(FiveAxisPoint, ThreeAxisPoint):
    '''x y z b c position of the nozzle. if any of xyzbc are not defined, the nozzle will not move in that 
    direction. optionally, for visualization purposes, color can be defined [r,g,b] [0-1,0-1,0-1] ...
    see PlotControls documentation for 'color_type'
    '''
    pass


class Printer(FiveAxisPrinter, ThreeAxisPrinter):
    'set print_speed and travel_speed of the 3D printer and the axis location. see documentation for info about other attributes'
    pass


class GcodeControls(FiveAxisGcodeControls, ThreeAxisGcodeControls):
    'control to adjust the style and initialization of the gcode'
    pass
