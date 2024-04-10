from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING
from fullcontrol.visualize.extrusion_classes import Extruder
from fullcontrol.visualize.bounding_box import BoundingBox
from fullcontrol.visualize.path import Path
from fullcontrol.visualize.controls import PlotControls

if TYPE_CHECKING:
    from fullcontrol.visualize.state import State
    from fullcontrol.visualize.plot_data import PlotData
    from fullcontrol.visualize.annotations import PlotAnnotation


class PlotData(BaseModel):
    '''
    A class representing a list of Paths (path.py), each with details about x, y, z values, [r,g,b] colors, and the 
    state of the extruder. A new path is created each time the extruder changes on/off. Data for 
    annotations of the plot and the bounding box enclosing all paths are also included. A list of 
    steps and pre-initialized State must be passed upon instantiation to allow initialization of 
    various attributes.

    Attributes:
        paths (Optional[list]): A list of Paths.
        bounding_box (Optional[BoundingBox]): The bounding box enclosing all paths.
        annotations (Optional[list]): A list of annotations for the plot.

    Methods:
        __init__(steps: list, state: 'State'): Initializes the PlotData object with the given steps and state.
        add_path(state: 'State', plot_data: 'PlotData', plot_controls: PlotControls): Adds a new path to the PlotData object.
        add_annotation(annotation: 'PlotAnnotation'): Adds an annotation to the PlotData object.
        cleanup(): Removes single-point paths from the PlotData object.
    '''
    paths: Optional[list] = []  # list of Paths
    bounding_box: Optional[BoundingBox] = BoundingBox()
    annotations: Optional[list] = []

    def __init__(self, steps: list, state: 'State'):
        """
            Initializes a PlotData object.

            Args:
                steps (list): A list of steps.
                state (State): The state object.

            Returns:
                None
            """
        super().__init__()
        # calculate and assign initial values in plot_data'
        self.bounding_box.calc_bounds(steps)
        self.paths.append(Path())
        state.path_count_now += 1  # increased since plot_data is initialised with 1 path
        self.paths[-1].extruder = Extruder(on=state.extruder.on)


    def add_path(self, state: 'State', plot_data: 'PlotData', plot_controls: PlotControls):
        """
        Adds a new path to the list of paths and updates the state, plot data, and plot controls.

        Args:
            state (State): The state object.
            plot_data (PlotData): The plot data object.
            plot_controls (PlotControls): The plot controls object.
        """
        self.paths.append(Path())
        state.point.update_color(state, plot_data, plot_controls)
        self.paths[-1].add_point(state)
        # self.paths[-1].colors.add_colors(state, plot_data)
        self.paths[-1].extruder = Extruder(on=state.extruder.on)

        
    def add_annotation(self, annotation: 'PlotAnnotation'):
        """
        Adds an annotation to the plot.

        Args:
            annotation (PlotAnnotation): The annotation to be added.

        Returns:
            None
        """
        self.annotations.append({'label': annotation.label, 'x': annotation.point.x, 'y': annotation.point.y, 'z': annotation.point.z})


    def cleanup(self):
        '''
        Remove single-point paths from the list of paths.

        Single-point paths can be caused by an Extruder at the end of the list or similar.

        Returns:
            None
        '''
        self.paths = [path for path in self.paths if len(path.xvals)>1]
