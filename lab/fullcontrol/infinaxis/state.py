from typing import Optional
from pydantic import BaseModel
from importlib import import_module

from fullcontrol.gcode.extrusion_classes import ExtrusionGeometry, Extruder
from fullcontrol.gcode import ManualGcode

from lab.fullcontrol.infinaxis.point import Point
from lab.fullcontrol.infinaxis.printer import Printer
from lab.fullcontrol.infinaxis.controls import GcodeControls


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
    distance_accumulated: Optional[float] = 0.0

    def __init__(self, steps: list, gcode_controls: GcodeControls):
        super().__init__()
        # initialize state based on the named-printer default initialization_data and initialization_data over-rides passed by designer in gcode_controls

        def first_infinaxis_point(steps: list, fully_defined: bool = True) -> Point:
            'return first Point in list. if the parameter fully_defined is true, return first Point with x,y,z'
            if type(steps).__name__ == 'list':
                for i in range(len(steps)):
                    if isinstance(steps[i], Point):
                        if fully_defined:
                            if steps[i].x != None and steps[i].y != None and steps[i].z != None:
                                return steps[i]
                        else:
                            return steps[i]
            if fully_defined:
                raise Exception(f'No point found in steps with fully defined x, y, and z')
            if not fully_defined:
                raise Exception(f'No point found in steps')

        # the following line was edited from 3-axis gcode since 5-axis gcode is output in a simple form for now
        initialization_data = import_module(f'fullcontrol.devices.community.singletool.generic').set_up(gcode_controls.initialization_data)

        self.extruder = Extruder(
            units=initialization_data['e_units'],
            dia_feed=initialization_data['dia_feed'],
            total_volume=0,
            total_volume_ref=0,
            on=True)  # on=True is different from 3-axis gcode since the primer has been disabled
        self.extruder.update_e_ratio()

        # Calculate post_ik_offset from bed center and chains

        post_ik_offset = Point(x=gcode_controls.bed_center.x,y=gcode_controls.bed_center.y,z=gcode_controls.bed_center.z)

        for link in gcode_controls.head_chain:
            post_ik_offset.x += link.offset.x
            post_ik_offset.y += link.offset.y
            post_ik_offset.z += link.offset.z
        
        for link in gcode_controls.bed_chain:
            post_ik_offset.x += -link.offset.x
            post_ik_offset.y += -link.offset.y
            post_ik_offset.z += -link.offset.z

        self.printer = Printer(
            command_list=initialization_data['printer_command_list'],
            print_speed=initialization_data['print_speed'],
            travel_speed=initialization_data['travel_speed'],
            head_chain=gcode_controls.head_chain,
            bed_chain=gcode_controls.bed_chain,
            xyz_orientation=gcode_controls.xyz_orientation,
            bed_center=gcode_controls.bed_center,
            post_ik_offset=post_ik_offset,
            inverse_time_feedrate=gcode_controls.inverse_time_feedrate,
            planning_axes_mono=gcode_controls.planning_axes_mono,
            planning_axes_tripple= gcode_controls.planning_axes_tripple,
            planning_axes_names= gcode_controls.planning_axes_names,
            verbose=gcode_controls.verbose,
            f_round=gcode_controls.f_round,
            speed_changed=True)

        self.extrusion_geometry = ExtrusionGeometry(
            area_model=initialization_data['area_model'],
            width=initialization_data['extrusion_width'],
            height=initialization_data['extrusion_height'])
        self.extrusion_geometry.update_area()

        # primer_steps = import_module(f'fullcontrol.gcode.primer_library.travel').primer(first_XYZBC_point(steps))
        primer_steps = []
        primer_steps.append(Extruder(on=False))
        primer_steps.append(first_infinaxis_point(steps))  # move fast to start position
        primer_steps.append(Extruder(on=True))

        # Inverse time feedrate is incompatible with using predefined starting and ending procedures as it changes the way F parameter is calculated.
        infinaxis_start_steps = []
        infinaxis_end_steps = []
        if gcode_controls.inverse_time_feedrate:
            infinaxis_start_steps.append(ManualGcode(text='G93 ; inverse time feedrate mode'))
            infinaxis_end_steps.append(ManualGcode(text='G94 ; unit pr minute mode (default)'))
        self.steps = initialization_data['starting_procedure_steps'] + infinaxis_start_steps + primer_steps + steps + infinaxis_end_steps + initialization_data['ending_procedure_steps']
