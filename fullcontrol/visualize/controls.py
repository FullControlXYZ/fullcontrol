
from typing import Optional
from pydantic import BaseModel


class PlotControls(BaseModel):
    'control to adjust the style of the plot'
    color_type: Optional[str] = 'z_gradient'
    line_width: Optional[float] = 2
    style: Optional[str] = None # 'tube'/'line'
    tube_type: Optional[str] = None # 'flow'/'cylinders'
    tube_sides: Optional[int] = None
    zoom: Optional[float] = 1
    hide_annotations: Optional[bool] = False
    hide_travel: Optional[bool] = False
    hide_axes: Optional[bool] = False
    neat_for_publishing: Optional[bool] = False
    raw_data: Optional[bool] = False
    printer_name: Optional[str] = 'generic'
    # initialization_data is information about initial printing conditions, which may be changed by the fullcontrol 'design', whereas the above attributes are never changed by the 'design'
    initialization_data: Optional[dict] = {}  # values passed for initialization_data overwrite the default initialization_data of the printer
