from typing import Optional
from fullcontrol.common import BaseModelPlus


class Printer(BaseModelPlus):
    """
    A class representing a 3D printer.

    Attributes:
        print_speed (Optional[int]): The speed at which the printer prints, in units per minute.
        travel_speed (Optional[int]): The speed at which the printer moves between printing locations, in units per minute.
    """
    print_speed: Optional[float] = None
    travel_speed: Optional[float] = None
