from typing import Optional
from pydantic import BaseModel
from importlib import import_module

# from fullcontrol.gcode.point import Point
# from fullcontrol.gcode.printer import Printer
from fullcontrol.gcode.extrusion_classes import ExtrusionGeometry, Extruder
from fullcontrol.gcode.controls import GcodeControls
from lab.fullcontrol.multiaxis.gcode.XYZB.point import Point
from lab.fullcontrol.multiaxis.gcode.XYZB.printer import Printer
from lab.fullcontrol.multiaxis.gcode.XYZB.controls import GcodeControls


class State(BaseModel):
    ''' this tracks the state of instances of interest adjusted in the list 
    of steps (points, extruder, etc.). some relevant shared variables and 
    initialisation methods are also included. a list of steps and 
    GcodeControls must be passed upon instantiation to allow initialization
    of various attributes
    '''

    extruder: Optional[Extruder] = None
    printer: Optional[Printer] = None
    extrusion_geometry: Optional[ExtrusionGeometry] = None
    steps: Optional[list] = None
    point: Optional[Point] = Point()
    point_systemXYZ: Optional[Point] = Point()
    i: Optional[int] = 0
    gcode: Optional[list] = []

    def __init__(self, steps: list, gcode_controls: GcodeControls):
        super().__init__()
        # initialize state based on the named-printer default initialization_data and initialization_data over-rides passed by designer in gcode_controls

        def first_XYZB_point(steps: list, fully_defined: bool = True) -> Point:
            'return first Point in list. if the parameter fully_defined is true, return first Point with all x,y,z,b != None'
            if type(steps).__name__ == 'list':
                for i in range(len(steps)):
                    if type(steps[i]).__name__ == 'Point':
                        if fully_defined:
                            if steps[i].x != None and steps[i].y != None and steps[i].z != None and steps[i].b != None:
                                return steps[i]
                        else:
                            return steps[i]
            if fully_defined:
                raise Exception(
                    f'No point found in steps with all of x y z b defined')
            if not fully_defined:
                raise Exception(f'No point found in steps')

        # the following line was edited from 3-axis gcode since 5-axis gcode is output in a simple form for now
        initialization_data = import_module(f'fullcontrol.devices.community.singletool.generic').set_up(
            gcode_controls.initialization_data)

        self.extruder = Extruder(
            units=initialization_data['e_units'],
            dia_feed=initialization_data['dia_feed'],
            total_volume=0,
            total_volume_ref=0,
            on=True)  # on=True is different from 3-axis gcode since the primer has been disabled
        self.extruder.update_e_ratio()

        self.printer = Printer(
            command_list=initialization_data['printer_command_list'],
            print_speed=initialization_data['print_speed'],
            travel_speed=initialization_data['travel_speed'],
            # this is added compared to 3-axis gcode
            b_offset_x=gcode_controls.b_offset_x,
            b_offset_z=gcode_controls.b_offset_z,
            speed_changed=True)

        self.extrusion_geometry = ExtrusionGeometry(
            area_model=initialization_data['area_model'],
            width=initialization_data['extrusion_width'],
            height=initialization_data['extrusion_height'])
        self.extrusion_geometry.update_area()

        # primer_steps = import_module(f'fullcontrol.gcode.primer_library.travel').primer(first_XYZBC_point(steps))
        primer_steps = []
        primer_steps.append(Extruder(on=False))
        # move fast to start position
        primer_steps.append(first_XYZB_point(steps))
        primer_steps.append(Extruder(on=True))
        self.steps = initialization_data['starting_procedure_steps'] + \
            primer_steps + steps + \
            initialization_data['ending_procedure_steps']
