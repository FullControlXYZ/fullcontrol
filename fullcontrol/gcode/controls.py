
from typing import Optional
from pydantic import BaseModel


class GcodeControls(BaseModel):
    """
    Control to adjust the style and initialization of the gcode.

    Attributes:
        printer_name (Optional[str]): The name of the printer. Defaults to 'generic'.
        initialization_data (Optional[dict]): Values passed for initialization_data overwrite the default initialization_data of the printer. Defaults to an empty dictionary.
        save_as (Optional[str]): The file name to save the gcode as. Defaults to None resulting in no file being saved.
        include_date (Optional[bool]): Whether to include the date in the filename. Defaults to True.
        always_print_F (Optional[bool]): If True include speed in every gcode line irrespective of wether it changed. Defaults to False.
        always_print_geometry (Optional[bool]): If True include x, y and z coordinate in every gcode line irrespective of wether each coordinate changed. Defaults to False.
    """
    printer_name: Optional[str] = None
    initialization_data: Optional[dict] = {} # values passed for initialization_data overwrite the default initialization_data of the printer
    save_as: Optional[str] = None
    include_date: Optional[bool] = True
    always_print_F: Optional[bool] = False
    always_print_geometry: Optional[bool] = False

    def initialize(self):
        if self.printer_name is None:
            self.printer_name = 'generic'
            print("warning: printer is not set - defaulting to 'generic', which does not initialize the printer with proper start gcode\n   - use fc.transform(..., controls=fc.GcodeControls(printer_name='generic') to disable this message or set it to a real printer name\n")

