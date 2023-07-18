from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING
# from fullcontrol.vis_OO2.color import PathColors, Color
from fullcontrol.common import Extruder, ExtrusionGeometry
from fullcontrol.visualize.point import Point

if TYPE_CHECKING:
    from fullcontrol.visualize.state import State


class Path(BaseModel):
    ' lists of x, y, z, and [r,g,b] values for a line to be plotted. plus info about the extruder state for the path'
    xvals: Optional[list] = []
    yvals: Optional[list] = []
    zvals: Optional[list] = []
    colors: Optional[list] = []  # [r,g,b]
    extruder: Optional[Extruder] = None
    widths: Optional[list] = []
    heights: Optional[list] = []

    def add_point(self, state: 'State'):
        'append a point to this path'
        self.xvals.append(state.point.x)
        self.yvals.append(state.point.y)
        self.zvals.append(state.point.z)
        self.colors.append(state.point.color)
        self.widths.append(state.extrusion_geometry.width)
        self.heights.append(state.extrusion_geometry.height)
