
from typing import Optional
from pydantic import BaseModel


class PlotControls(BaseModel):
    'control to adjust the style of the plot'
    color_type: Optional[str] = 'z_gradient'
    line_width: Optional[float] = 2
    zoom: Optional[float] = 1
    hide_annotations: Optional[bool] = False
    hide_travel: Optional[bool] = False
    hide_axes: Optional[bool] = False
    neat_for_publishing: Optional[bool] = False
    raw_data: Optional[bool] = False
