from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel
from fullcontrol.common import Point
from fullcontrol.visualize.controls import PlotControls

if TYPE_CHECKING:
    from fullcontrol.visualize.state import State
    from fullcontrol.visualize.plot_data import PlotData


class PlotAnnotation(BaseModel):
    '''
    Represents an annotation for a plot.

    Attributes:
        point (Optional[Point]): The xyz point associated with the annotation. If not defined, the previous point in the list of steps before this annotation was defined is used.
        label (Optional[str]): The label text to be shown on the plot.

    Methods:
        visualize(state: 'State', plot_data: 'PlotData', plot_controls: PlotControls) -> None:
            Process a PlotAnnotation in a list of steps supplied by the designer to update plot_data and state.
    '''
    point: Optional[Point] = None
    label: Optional[str] = None

    def visualize(self, state: 'State', plot_data: 'PlotData', plot_controls: PlotControls) -> None:
        '''
        Process a PlotAnnotation in a list of steps supplied by the designer to update plot_data and state.

        Args:
            state ('State'): The current state of the plot.
            plot_data ('PlotData'): The data associated with the plot.
            plot_controls (PlotControls): The controls for the plot.

        Returns:
            None
        '''
        if self.point == None:
            self.point = Point(x=state.point.x, y=state.point.y, z=state.point.z)
        plot_data.add_annotation(self)
