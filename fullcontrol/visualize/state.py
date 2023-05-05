from typing import Optional
from pydantic import BaseModel

from fullcontrol.common import Point, Extruder
from fullcontrol.visualize.point import Point


class State(BaseModel):
    ''' this tracks the state of instances of interest adjusted in the list 
    of steps (points, extruder, etc.). some relevant shared variables and 
    initialisation methods are also included. a list of steps must be passed
    upon instantiation to allow initialization of point_count_total.
    '''
    point: Optional[Point] = Point()
    extruder: Optional[Extruder] = Extruder(on=True)
    path_count_now: Optional[int] = 0
    point_count_now: Optional[int] = 0
    point_count_total: Optional[int]

    def count_points(self, steps: list):
        return sum(1 for step in steps if isinstance(step, Point))

    def __init__(self, steps: list):
        super().__init__()
        self.point_count_total = self.count_points(steps)
