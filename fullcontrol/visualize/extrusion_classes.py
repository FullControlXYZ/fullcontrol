
from fullcontrol.common import Extruder as BaseExtruder
from typing import TYPE_CHECKING
from fullcontrol.visualize.controls import PlotControls

if TYPE_CHECKING:
    from fullcontrol.visualize.state import State
    from fullcontrol.visualize.plot_data import PlotData


class Extruder(BaseExtruder):
    'generic Extruder with a visualisation method added'

    def visualize(self, state: 'State', plot_data: 'PlotData', plot_controls: PlotControls):
        'process an Extruder in a list of steps supplied by the designer to update plot_data and state'
        if self.on != None and self.on != state.extruder.on:
            state.extruder.on = self.on
            # if path has more than one point in it (so there is at least a single line plotted), add new path, otherwise change state of the current path
            if len(plot_data.paths[-1].xvals) > 1:
                plot_data.add_path(state, plot_data, plot_controls)
                state.path_count_now += 1
            else:
                plot_data.paths[-1].extruder.on = self.on
