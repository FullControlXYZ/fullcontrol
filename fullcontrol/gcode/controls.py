
from typing import Optional
from pydantic import BaseModel


class GcodeControls(BaseModel):
    'control to adjust the style and initialization of the gcode'
    printer_name: Optional[str] = 'generic'
    initialization_data: Optional[dict] = {}  # values passed for initialization_data overwrite the default initialization_data of the printer
    save_as: Optional[str] = None
    include_date: Optional[bool] = True
