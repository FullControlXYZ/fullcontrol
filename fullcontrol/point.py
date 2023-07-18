from typing import Optional
from fullcontrol.common import BaseModelPlus


class Point(BaseModelPlus):
    'point with x y z cartesian components'
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
