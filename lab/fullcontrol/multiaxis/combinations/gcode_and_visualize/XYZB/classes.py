from lab.fullcontrol.multiaxis.gcode.XYZB.point import Point as FourAxisPoint
from fullcontrol.combinations.gcode_and_visualize.classes import Point as ThreeAxisPoint
from lab.fullcontrol.multiaxis.gcode.XYZB.printer import Printer as FourAxisPrinter
from fullcontrol.combinations.gcode_and_visualize.classes import Printer as ThreeAxisPrinter
from lab.fullcontrol.multiaxis.gcode.XYZB.controls import GcodeControls as FourAxisGcodeControls
from fullcontrol.combinations.gcode_and_visualize.common import GcodeControls as ThreeAxisGcodeControls


class Point(FourAxisPoint, ThreeAxisPoint):
    '''x y z b position of the nozzle. if any of xyzb are not defined, the nozzle will not move in that 
    direction. optionally, for visualization purposes, color can be defined [r,g,b] [0-1,0-1,0-1] ...
    see PlotControls documentation for 'color_type'
    '''
    pass


class Printer(FourAxisPrinter, ThreeAxisPrinter):
    'set print_speed and travel_speed of the 3D printer and the axis location. see documentation for info about other attributes'
    pass


class GcodeControls(FourAxisGcodeControls, ThreeAxisGcodeControls):
    'control to adjust the style and initialization of the gcode'
    pass
