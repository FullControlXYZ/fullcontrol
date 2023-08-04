from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel
from fullcontrol.common import Point
from fullcontrol.visualize.controls import PlotControls

if TYPE_CHECKING:
    from fullcontrol.visualize.state import State
    from fullcontrol.visualize.plot_data import PlotData


class PlotAnnotation(BaseModel):
    '''xyz point and label text to be shown on a plot. if the point is not defined, the 
    previous point in the list of steps before this annotation was defined is used
    '''
    point: Optional[Point] = None
    label: Optional[str] = None

    def visualize(self, state: 'State', plot_data: 'PlotData', plot_controls: PlotControls):
        'process a PlotAnnotation in a list of steps supplied by the designer to update plot_data and state'
        if self.point == None:
            self.point = Point(x=state.point.x, y=state.point.y, z=state.point.z)
        plot_data.add_annotation(self)
