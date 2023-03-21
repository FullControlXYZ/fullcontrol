
from pydantic import BaseModel
from typing import Optional


class BoundingBox(BaseModel):
    'geometric measures of a bounding box, inlcuding mid values and ranges'
    minx: Optional[float]
    midx: Optional[float]
    maxx: Optional[float]
    # ranges and mid values are included as attributes, even though they are simple, to avoid them
    # being calculated for every point for the color_type z_gradient
    rangex: Optional[float]
    miny: Optional[float]
    midy: Optional[float]
    maxy: Optional[float]
    rangey: Optional[float]
    minz: Optional[float]
    midz: Optional[float]
    maxz: Optional[float]
    rangez: Optional[float]

    def calc_bounds(self, steps):
        'calculate the bounds and other useful geometric measures of the bounding box for all points in a list of steps'
        self.minx = 1e10  # initial high value always overwritten
        self.miny = 1e10  # initial high value always overwritten
        self.minz = 1e10  # initial high value always overwritten
        self.maxx = -1e10  # initial low value always overwritten
        self.maxy = -1e10  # initial low value always overwritten
        self.maxz = -1e10  # initial low value always overwritten
        for i in range(len(steps)):
            if type(steps[i]).__name__ == 'Point':
                if steps[i].x != None:
                    self.minx = min(self.minx, steps[i].x)
                if steps[i].y != None:
                    self.miny = min(self.miny, steps[i].y)
                if steps[i].z != None:
                    self.minz = min(self.minz, steps[i].z)
                if steps[i].x != None:
                    self.maxx = max(self.maxx, steps[i].x)
                if steps[i].y != None:
                    self.maxy = max(self.maxy, steps[i].y)
                if steps[i].z != None:
                    self.maxz = max(self.maxz, steps[i].z)
        self.midx = (self.minx + self.maxx) / 2
        self.midy = (self.miny + self.maxy) / 2
        self.midz = (self.minz + self.maxz) / 2
        self.rangex = (self.maxx - self.minx)
        self.rangey = (self.maxy - self.miny)
        self.rangez = (self.maxz - self.minz)
