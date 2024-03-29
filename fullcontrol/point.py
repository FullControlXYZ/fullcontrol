from typing import Optional
from fullcontrol.common import BaseModelPlus


class Point(BaseModelPlus):
    """Represents a point in 3D space with x, y, and z cartesian components."""
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
