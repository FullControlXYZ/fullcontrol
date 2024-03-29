
from typing import Optional
from pydantic import BaseModel


class GcodeControls(BaseModel):
    """
    Control to adjust the style and initialization of the gcode.

    Attributes:
        printer_name (Optional[str]): The name of the printer. Defaults to 'generic'.
        initialization_data (Optional[dict]): Values passed for initialization_data overwrite the default initialization_data of the printer. Defaults to an empty dictionary.
        save_as (Optional[str]): The file name to save the gcode as. Defaults to None.
        include_date (Optional[bool]): Whether to include the date in the gcode. Defaults to True.
    """
    printer_name: Optional[str] = 'generic'
    initialization_data: Optional[dict] = {} # values passed for initialization_data overwrite the default initialization_data of the printer
    save_as: Optional[str] = None
    include_date: Optional[bool] = True
