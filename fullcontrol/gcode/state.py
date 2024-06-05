from typing import Optional
from pydantic import BaseModel
from importlib import import_module

from fullcontrol.gcode.point import Point
from fullcontrol.gcode.printer import Printer
from fullcontrol.gcode.extrusion_classes import ExtrusionGeometry, Extruder
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.common import first_point
from fullcontrol.gcode.import_printer import import_printer


class State(BaseModel):
    '''
    This class tracks the state of instances of interest adjusted in the list 
    of steps (points, extruder, etc.). It also includes some relevant shared variables and 
    initialization methods. Upon instantiation, a list of steps and GcodeControls must be passed
    to allow initialization of various attributes.

    Attributes:
        extruder (Optional[Extruder]): The extruder instance.
        printer (Optional[Printer]): The printer instance.
        extrusion_geometry (Optional[ExtrusionGeometry]): The extrusion geometry instance.
        steps (Optional[list]): The list of steps.
        point (Optional[Point]): The current point.
        i (Optional[int]): The current index.
        gcode (Optional[list]): The list of Gcode.

    Methods:
        __init__: Initializes the State object.

    '''

    extruder: Optional[Extruder] = None
    printer: Optional[Printer] = None
    extrusion_geometry: Optional[ExtrusionGeometry] = None
    steps: Optional[list] = None
    point: Optional[Point] = Point()
    i: Optional[int] = 0
    gcode: Optional[list] = []

    def __init__(self, steps: list, gcode_controls: GcodeControls):
        """
        Initializes a State object.

        Args:
            steps (list): A list of steps for the state.
            gcode_controls (GcodeControls): An instance of the GcodeControls class.

        Returns:
            None
        """
        super().__init__()
        # initialize state based on the named-printer default initialization_data and initialization_data over-rides passed by designer in gcode_controls

        if gcode_controls.printer_name[:5] == 'Cura/' or gcode_controls.printer_name[:10] == 'Community/':
            initialization_data = import_printer(gcode_controls.printer_name, gcode_controls.initialization_data)
            # note if using 'no_primer' there is a risk that no initial Point is defined before the first G1 command meaning length calculation for the line is impossible and an error will occur
        else:
            initialization_data = import_module(f'fullcontrol.devices.community.singletool.{gcode_controls.printer_name}').set_up(gcode_controls.initialization_data)

        self.extruder = Extruder(
            units=initialization_data['e_units'],
            dia_feed=initialization_data['dia_feed'],
            total_volume=0,
            total_volume_ref=0,
            travel_format=initialization_data['travel_format'])
        self.extruder.update_e_ratio()
        if initialization_data['manual_e_ratio'] != None:
            self.extruder.volume_to_e = initialization_data['manual_e_ratio']

        self.printer = Printer(
            command_list=initialization_data['printer_command_list'],
            print_speed=initialization_data['print_speed'],
            travel_speed=initialization_data['travel_speed'],
            speed_changed=True)

        self.extrusion_geometry = ExtrusionGeometry(
            area_model=initialization_data['area_model'],
            width=initialization_data['extrusion_width'],
            height=initialization_data['extrusion_height'])
        self.extrusion_geometry.update_area()

        primer_steps = import_module(f'fullcontrol.gcode.primer_library.{initialization_data["primer"]}').primer(first_point(steps))
        self.steps = initialization_data['starting_procedure_steps'] + primer_steps + steps + initialization_data['ending_procedure_steps']
