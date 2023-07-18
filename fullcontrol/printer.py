from typing import Optional
from fullcontrol.common import BaseModelPlus


class Printer(BaseModelPlus):
    'set print_speed and travel_speed of the 3D printer.'

    print_speed: Optional[int] = None
    travel_speed: Optional[int] = None
