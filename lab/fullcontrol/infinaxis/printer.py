from typing import Optional
from fullcontrol import Printer as BasePrinter
from fullcontrol import Point


class Printer(BasePrinter):
    'generic gcode Printer with infinaxis aspects added/modified'
    bed_center: Point = None
    post_ik_offset: Point = None
    head_chain: list = None
    bed_chain: list = None
    xyz_orientation: list = None
    inverse_time_feedrate: bool = None  # if true, F command will be output as inverse time feedrate (e.g. F2 for 30 seconds per move (1/2 minutes per move)) instead of speed (e.g. F300 for 300 mm/s). This is useful for some multiaxis machines that use inverse time feedrate to control speed.
    planning_axes_mono: bool = None
    planning_axes_tripple: bool = None
    planning_axes_names: list[str] = None
    verbose: bool = None
    f_round: bool = None