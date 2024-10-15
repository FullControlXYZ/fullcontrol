
from fullcontrol.common import Extruder as BaseExtruder
from fullcontrol.common import ExtrusionGeometry as BaseExtrusionGeometry
from typing import TYPE_CHECKING
from fullcontrol.visualize.controls import PlotControls

if TYPE_CHECKING:
    from fullcontrol.visualize.state import State
    from fullcontrol.visualize.plot_data import PlotData


class Extruder(BaseExtruder):
    'Extend generic class with visualize method to convert the object to visualisation data'


    def visualize(self, state: 'State', plot_data: 'PlotData', plot_controls: PlotControls):
        '''
        Process an Extruder in a list of steps supplied by the designer to update plot_data and state.

        Args:
            state (State): The current state of the extruder.
            plot_data (PlotData): The data used for plotting.
            plot_controls (PlotControls): The controls for plotting.

        Returns:
            None
        '''
        if self.on != None and self.on != state.extruder.on:
            state.extruder.on = self.on
            # if path has more than one point in it (so there is at least a single line plotted), add new path, otherwise change state of the current path
            if len(plot_data.paths[-1].xvals) > 1:
                plot_data.add_path(state, plot_data, plot_controls)
                state.path_count_now += 1
            else:
                plot_data.paths[-1].extruder.on = self.on
                state.point.update_color(state, plot_data, plot_controls)
                if len(plot_data.paths[-1].colors) > 0: plot_data.paths[-1].colors[-1] = state.point.color


class ExtrusionGeometry(BaseExtrusionGeometry):
    'Extend generic class with visualize method to convert the object to visualisation data'

    def visualize(self, state: 'State', plot_data: 'PlotData', plot_controls: PlotControls):
        '''
        Process an Extrusion_Geometry in a list of steps supplied by the designer to update state.

        Args:
            state (State): The state object to be updated.
            plot_data (PlotData): The plot data object.
            plot_controls (PlotControls): The plot controls object.
        '''
        from math import pi 
        if self.width != None and self.width != state.extrusion_geometry.width:
            state.extrusion_geometry.width = round(self.width, 3)
        if self.height != None and self.height != state.extrusion_geometry.height:
            state.extrusion_geometry.height = round(self.height, 3)
        if self.diameter != None:
            state.extrusion_geometry.width = round(self.diameter, 3)
            state.extrusion_geometry.height = round(self.diameter, 3)
        if self.area != None:
            dia = 2*(self.area/pi)**0.5
            state.extrusion_geometry.width = round(dia, 3)
            state.extrusion_geometry.height = round(dia, 3)

    
