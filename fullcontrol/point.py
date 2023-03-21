from typing import Optional
from fullcontrol.common import BaseModelPlus


class Point(BaseModelPlus):
    'point with x y z cartesian components'
    x: Optional[float]
    y: Optional[float]
    z: Optional[float]
