

import fullcontrol.gcode as gc
import fullcontrol.visualize as vis
from fullcontrol.base import BaseModelPlus


# inherit attributes to generate both gcode and visualization data

# rather than manually writing all of the objects below, it would be great if this was automated. That
# would allow a used to add an extra object in the gcode subpackage, but not have to worry about adding
# it here. this automation would need some consideration to get an appropriate docstring for each class

# 1. classes used to add a visualize or gcode method to class that simply passes

class PassGcode(BaseModelPlus):
    def gcode(self, state): pass


class PassVisualize(BaseModelPlus):
    def visualize(self, state, plot_data, plot_controls): pass


# 2. combined classes that are defined in both gcode and visualization subpackages

class Point(gc.Point, vis.Point):
    '''x y z position of the nozzle. if any of xyz are not defined, the nozzle will not move in that 
    direction. optionally, for visualization purposes, color can be defined [r,g,b] [0-1,0-1,0-1] ...
    see PlotControls documentation for 'color_type'
    '''
    pass


class Extruder(gc.Extruder, vis.Extruder):
    '''set the state of the extruder with the 'on' attribute (True or False). see documentation for info about other attributes
    '''
    pass


class ExtrusionGeometry(gc.ExtrusionGeometry, vis.ExtrusionGeometry):
    ''' geometric description of the printed extrudate. 'area_model' is used to specify how cross-sectional
    area of the extrudate is defined. area_model options: rectangle (requires width and height) / stadium 
    (requires width and height) / circle (requires diameter) / manual (requires area attribute to be set
    manually). the 'area' attribute is automatically calculated unless area_model=='manual' 
    '''
    pass

# 3. classes that are defined in the gcode subpackage only


class PrinterCommand(gc.PrinterCommand, PassVisualize):
    'state the id of the printer command that should be executed ... manifesting in an appropriate line of gcode'
    pass


class ManualGcode(gc.ManualGcode, PassVisualize):
    "custom gcode defined by 'text' attribute will be added as a new line of gcode"
    pass


class Printer(gc.Printer, PassVisualize):
    'set print_speed and travel_speed of the 3D printer. see documentation for info about other attributes'
    pass


class Fan(gc.Fan, PassVisualize):
    'fan speed percent (0-100)'
    pass


class Hotend(gc.Hotend, PassVisualize):
    '''set temperature of hotend. if wait==True, system will wait for temperature to be reached
    before continuing. tool number can be defined for multi-tool printers
    '''
    pass


class Buildplate(gc.Buildplate, PassVisualize):
    'set temperature of the buildplate. if wait==True, system will wait for temperature to be reached before continuing'
    pass


class StationaryExtrusion(gc.StationaryExtrusion, PassVisualize):
    'extrude a set volume of material at the set speed while the nozzle is stationary. negative volumes indicate retraction'
    pass


class GcodeComment(gc.GcodeComment, PassVisualize):
    '''use the 'text' attribute to add a comment as a new line gcode. use the 'end_of_previous_line_text' attribute 
    to add a comment to the end of the line of gcode produced by the previous step'''
    pass


class GcodeControls(gc.GcodeControls, PassVisualize):
    'control to adjust the style and initialization of the gcode'
    pass

# 4. classes that are defined in the visualization subpackage only


class PlotAnnotation(vis.PlotAnnotation, PassGcode):
    '''xyz point and label text to be shown on a plot. if the point is not defined, the 
    previous point in the list of steps before this annotation was defined is used
    '''
    pass


class PlotControls(vis.PlotControls, PassGcode):
    'control to adjust the style of the plot - see documentation for details about allowable values'
    pass
