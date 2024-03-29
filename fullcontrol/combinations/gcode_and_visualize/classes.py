

import fullcontrol.gcode as gc
import fullcontrol.visualize as vis
from fullcontrol.base import BaseModelPlus


# inherit attributes to generate both gcode and visualization data

# rather than manually writing all of the objects below, it would be great if this was automated. That
# would allow a used to add an extra object in the gcode subpackage, but not have to worry about adding
# it here. this automation would need some consideration to get an appropriate docstring for each class

# 1. classes used to add a visualize or gcode method to class that simply passes

class PassGcode(BaseModelPlus):
    """A class representing a pass Gcode."""

    def gcode(self, state):
        """Generate Gcode based on the given state.

        Args:
            state: The state of the pass.

        Returns:
            The generated Gcode.
        """
        pass


class PassVisualize(BaseModelPlus):
    """
    A class for visualizing the state, plot data, and plot controls.

    Attributes:
        state (State): The state object containing the current state information.
        plot_data (PlotData): The plot data object containing the data to be plotted.
        plot_controls (PlotControls): The plot controls object containing the settings for plotting.

    Methods:
        visualize(): Visualizes the state, plot data, and plot controls.
    """

    def visualize(self, state, plot_data, plot_controls):
        """
        Visualizes the state, plot data, and plot controls.

        Args:
            state (State): The state object containing the current state information.
            plot_data (PlotData): The plot data object containing the data to be plotted.
            plot_controls (PlotControls): The plot controls object containing the settings for plotting.
        """
        pass


# 2. combined classes that are defined in both gcode and visualization subpackages

class Point(gc.Point, vis.Point):
    '''
    Represents the x, y, z position of the nozzle.

    If any of the x, y, or z coordinates are not defined, the nozzle will not move in that direction.

    Optionally, for visualization purposes, the color can be defined as [r, g, b] where each value is in the range of 0-1.
    See the PlotControls documentation for the 'color_type' parameter.

    Attributes:
        x (float): The x-coordinate of the nozzle position.
        y (float): The y-coordinate of the nozzle position.
        z (float): The z-coordinate of the nozzle position.
        color (list): The color of the nozzle for visualization purposes.

    '''
    pass


class Extruder(gc.Extruder, vis.Extruder):
    '''A class representing an extruder.

    This class inherits from `gc.Extruder` and `vis.Extruder` classes.

    Attributes:
        on (bool): The state of the extruder. Set to True for on and False for off.

    Note:
        For more information about other attributes, please refer to the documentation.
    '''
    pass


class ExtrusionGeometry(gc.ExtrusionGeometry, vis.ExtrusionGeometry):
    ''' 
    Geometric description of the printed extrudate. 'area_model' is used to specify how cross-sectional
    area of the extrudate is defined. 

    area_model options: 
    - rectangle (requires width and height) 
    - stadium (requires width and height) 
    - circle (requires diameter) 
    - manual (requires area attribute to be set manually). 

    The 'area' attribute is automatically calculated unless area_model=='manual'. 
    '''
    pass

# 3. classes that are defined in the gcode subpackage only


class PrinterCommand(gc.PrinterCommand, PassVisualize):
    '''
    Represents a printer command that should be executed, manifesting in an appropriate line of gcode.

    This class inherits from `gc.PrinterCommand` and `PassVisualize`.
    '''

    pass


class ManualGcode(gc.ManualGcode, PassVisualize):
    """
    Custom Gcode class that allows adding a new line of Gcode defined by the 'text' attribute.

    Attributes:
        text (str): The custom Gcode line to be added.
    """
    pass


class Printer(gc.Printer, PassVisualize):
    '''
    A class that represents a 3D printer.

    Inherits from `gc.Printer` and `PassVisualize`.

    Attributes:
        print_speed (float): The speed at which the printer prints.
        travel_speed (float): The speed at which the printer moves between print locations.

    Note: For more information about other attributes, please refer to the documentation.
    '''
    pass


class Fan(gc.Fan, PassVisualize):
    '''
    Represents a fan with a speed percentage.

    Attributes:
        - speed (int): The speed of the fan as a percentage (0-100).
    '''
    pass


class Hotend(gc.Hotend, PassVisualize):
    '''set temperature of hotend. if wait==True, system will wait for temperature to be reached
    before continuing. tool number can be defined for multi-tool printers
    
    Args:
        gc.Hotend: The base class for the hotend.
        PassVisualize: The base class for visualization.
    '''
    pass


class Buildplate(gc.Buildplate, PassVisualize):
    '''A class representing a buildplate.

    This class inherits from `gc.Buildplate` and `PassVisualize` classes.

    Attributes:
        None

    Methods:
        None
    '''
    pass


class StationaryExtrusion(gc.StationaryExtrusion, PassVisualize):
    '''
    Extrude a set volume of material at the set speed while the nozzle is stationary.
    Negative volumes indicate retraction.
    '''
    pass


class GcodeComment(gc.GcodeComment, PassVisualize):
    '''
    A class that represents a Gcode comment.

    Attributes:
        text (str): The comment text to be added as a new line of Gcode.
        end_of_previous_line_text (str): The comment text to be added at the end of the line of Gcode produced by the previous step.
    '''
    pass


class GcodeControls(gc.GcodeControls, PassVisualize):
    '''
    Control class to adjust the style and initialization of the gcode.

    This class inherits from `gc.GcodeControls` and `PassVisualize`.
    '''

    pass

# 4. classes that are defined in the visualization subpackage only


class PlotAnnotation(vis.PlotAnnotation, PassGcode):
    '''xyz point and label text to be shown on a plot. if the point is not defined, the 
    previous point in the list of steps before this annotation was defined is used
    
    Attributes:
        - point: The XYZ coordinates of the annotation point.
        - label: The text label to be shown for the annotation.
    '''
    pass


class PlotControls(vis.PlotControls, PassGcode):
    '''
    Control to adjust the style of the plot.

    This class inherits from `vis.PlotControls` and `PassGcode`. It provides a way to adjust the style of the plot.
    Please refer to the documentation for more details about the allowable values.
    '''
    pass
