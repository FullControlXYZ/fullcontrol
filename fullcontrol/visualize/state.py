from typing import Optional
from pydantic import BaseModel
from importlib import import_module

from fullcontrol.common import Point, Extruder, ExtrusionGeometry
from fullcontrol.visualize.point import Point
from fullcontrol.visualize.controls import PlotControls


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
    point_count_total: Optional[int] = None
    extrusion_geometry: Optional[ExtrusionGeometry] = None

    def count_points(self, steps: list):
        return sum(1 for step in steps if isinstance(step, Point))

    def __init__(self, steps: list, plot_controls: PlotControls):
        super().__init__()
        self.point_count_total = self.count_points(steps)

        initialization_data = import_module(f'fullcontrol.gcode.printer_library.singletool.{plot_controls.printer_name}').set_up(
            plot_controls.initialization_data)  # future plan: move printer library from gcode package since it can affect more than just gcode

        self.extrusion_geometry = ExtrusionGeometry(
            width=initialization_data['extrusion_width'],
            height=initialization_data['extrusion_height'])
        self.extrusion_geometry.update_area()
