from pydantic import BaseModel
from typing import Optional
# from fullcontrol.vis_OO2.color import PathColors, Color
from fullcontrol.common import Extruder
from fullcontrol.visualize.point import Point


class Path(BaseModel):
    ' lists of x, y, z, and [r,g,b] values for a line to be plotted. plus info about the extruder state for the path'
    xvals: Optional[list] = []
    yvals: Optional[list] = []
    zvals: Optional[list] = []
    colors: Optional[list] = []  # [r,g,b]
    extruder: Optional[Extruder]

    def add_point(self, point: Point):
        'append a point to this path'
        self.xvals.append(point.x)
        self.yvals.append(point.y)
        self.zvals.append(point.z)
        self.colors.append(point.color)
