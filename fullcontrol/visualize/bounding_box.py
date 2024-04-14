from pydantic import BaseModel
from typing import Optional

from fullcontrol.common import Point


class BoundingBox(BaseModel):
    '''
    Represents the geometric measures of a bounding box, including mid values and ranges.

    Attributes:
        minx (Optional[float]): The minimum x-coordinate of the bounding box.
        midx (Optional[float]): The mid x-coordinate of the bounding box.
        maxx (Optional[float]): The maximum x-coordinate of the bounding box.
        rangex (Optional[float]): The range of x-coordinates in the bounding box.
        miny (Optional[float]): The minimum y-coordinate of the bounding box.
        midy (Optional[float]): The mid y-coordinate of the bounding box.
        maxy (Optional[float]): The maximum y-coordinate of the bounding box.
        rangey (Optional[float]): The range of y-coordinates in the bounding box.
        minz (Optional[float]): The minimum z-coordinate of the bounding box.
        midz (Optional[float]): The mid z-coordinate of the bounding box.
        maxz (Optional[float]): The maximum z-coordinate of the bounding box.
        rangez (Optional[float]): The range of z-coordinates in the bounding box.
    '''

    minx: Optional[float] = None
    midx: Optional[float] = None
    maxx: Optional[float] = None
    # ranges and mid values are included as attributes, even though they are simple, to avoid them
    # being calculated for every point for the color_type z_gradient
    rangex: Optional[float] = None
    miny: Optional[float] = None
    midy: Optional[float] = None
    maxy: Optional[float] = None
    rangey: Optional[float] = None
    minz: Optional[float] = None
    midz: Optional[float] = None
    maxz: Optional[float] = None
    rangez: Optional[float] = None

    def calc_bounds(self, steps):
        '''
        Calculate the bounds and other useful geometric measures of the bounding box for all points in a list of steps.

        Args:
            steps (List[Point]): A list of points representing the steps.

        Returns:
            None
        '''
        self.minx = 1e10  # initial high value always overwritten
        self.miny = 1e10  # initial high value always overwritten
        self.minz = 1e10  # initial high value always overwritten
        self.maxx = -1e10  # initial low value always overwritten
        self.maxy = -1e10  # initial low value always overwritten
        self.maxz = -1e10  # initial low value always overwritten
        for step in steps:
            if isinstance(step, Point):
                if (x := step.x) is not None:
                    self.minx = min(self.minx, x)
                    self.maxx = max(self.maxx, x)
                if (y := step.y) is not None:
                    self.miny = min(self.miny, y)
                    self.maxy = max(self.maxy, y)
                if (z := step.z) is not None:
                    self.minz = min(self.minz, z)
                    self.maxz = max(self.maxz, z)
        self.midx = (self.minx + self.maxx) / 2
        self.midy = (self.miny + self.maxy) / 2
        self.midz = (self.minz + self.maxz) / 2
        self.rangex = (self.maxx - self.minx)
        self.rangey = (self.maxy - self.miny)
        self.rangez = (self.maxz - self.minz)
