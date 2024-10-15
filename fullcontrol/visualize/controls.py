
from typing import Optional
from pydantic import BaseModel


class PlotControls(BaseModel):
    """
    Control class to adjust the style of the plot.

    Attributes:
        color_type (Optional[str]): The type of color gradient to use. Default is 'z_gradient'. Options are 'manual', 'random_blue', 'z_gradient', 'print_sequence' and 'print_sequence_fluctuating'
        line_width (Optional[float]): The width of the lines in the plot. Default is 2.
        style (Optional[str]): The style of the plot. Can be 'tube' or 'line'. Default is None.
        tube_type (Optional[str]): The type of tube to use. Can be 'flow' or 'cylinders'. Default is 'flow'.
        tube_sides (Optional[int]): The number of sides of the tube. Default is 4.
        zoom (Optional[float]): The zoom level of the plot. Default is 1.
        hide_annotations (Optional[bool]): Whether to hide annotations in the plot. Default is False.
        hide_travel (Optional[bool]): Whether to hide travel lines in the plot. Default is False.
        hide_axes (Optional[bool]): Whether to hide axes in the plot. Default is False.
        neat_for_publishing (Optional[bool]): Whether to optimize the plot for publishing. Default is False.
        raw_data (Optional[bool]): Whether to show raw data in the plot. Default is False.
        printer_name (Optional[str]): The name of the printer. Default is 'generic'.
        initialization_data (Optional[dict]): Information about initial printing conditions. Default is an empty dictionary. Values passed for initialization_data overwrite the default initialization_data of the printer.
    """
    color_type: Optional[str] = 'z_gradient'
    line_width: Optional[float] = None
    style: Optional[str] = None # 'tube'/'line'
    tube_type: Optional[str] = 'flow'  # 'flow'/'cylinders'
    tube_sides: Optional[int] = 4
    zoom: Optional[float] = 1
    hide_annotations: Optional[bool] = False
    hide_travel: Optional[bool] = False
    hide_axes: Optional[bool] = False
    neat_for_publishing: Optional[bool] = False
    raw_data: Optional[bool] = False
    printer_name: Optional[str] = 'generic'
    # initialization_data is information about initial printing conditions, which may be changed by the fullcontrol 'design', whereas the above attributes are never changed by the 'design'
    initialization_data: Optional[dict] = {}  # values passed for initialization_data overwrite the default initialization_data of the printer

    def initialize(self):
        if not self.raw_data: # the follows defaults are only required if plotting the path, not for raw data export
            if self.style is None:
                self.style = 'tube'
                print("warning: plot style is not set - defaulting to 'tube', which shows simulated printed line width and height\n    - use fc.transform(..., controls=fc.PlotControls(style='tube') to disable this message or style='line' for a simpler line preview\n")
            if self.style == 'tube' and self.line_width is not None:
                print("warning: `line_width` for the plot is set, but the plot style is 'tube' \n   - `line_width` will be ignored except for non-extruding travel lines... extruded lines are previewed with the real designed width and height\n")
            if self.line_width is None:
                self.line_width = 2