from fullcontrol.gcode import Point, Printer, Extruder, ManualGcode, PrinterCommand, GcodeComment, Buildplate, Hotend, Fan, StationaryExtrusion
import fullcontrol.devices.community.singletool.base_settings as base_settings

# 'chamber temp' could be incorperated into FullControl as a new state object, since the designer may wish to change this during the printing procedure
# 'include_purge' and 'z_offset' could be included as built-in attributes of GcodeControls


def set_up(user_overrides: dict):
    ''' DO THIS
    '''

    # overrides for this specific printer relative those defined in base_settings.py
    printer_overrides = {'primer': 'travel', 'chamber_temp': 50, 'z_offset': None, 'include_purge': True}
    # update default initialization settings with printer-specific overrides and user-defined overrides
    initialization_data = {**base_settings.default_initial_settings, **printer_overrides}
    initialization_data = {**initialization_data, **user_overrides}

    starting_procedure_steps = []
    starting_procedure_steps.append(ManualGcode(
        text='; Time to print!!!!!\n; GCode created with FullControl - tell us what you\'re printing!\n; info@fullcontrol.xyz or tag FullControlXYZ on Twitter/Instagram/LinkedIn/Reddit/TikTok \n'))
    starting_procedure_steps.append(ManualGcode(text='print_start EXTRUDER=' + str(initialization_data["nozzle_temp"]) + ' BED='+str(
        initialization_data["bed_temp"]) + ' CHAMBER=' + str(initialization_data['chamber_temp'])))
    starting_procedure_steps.append(PrinterCommand(id='absolute_coords'))
    starting_procedure_steps.append(PrinterCommand(id='units_mm'))
    starting_procedure_steps.append(Extruder(relative_gcode=initialization_data["relative_e"]))
    starting_procedure_steps.append(Fan(speed_percent=initialization_data["fan_percent"]))
    starting_procedure_steps.append(ManualGcode(
        text='M220 S' + str(initialization_data["print_speed_percent"])+' ; set speed factor override percentage'))
    starting_procedure_steps.append(ManualGcode(
        text='M221 S' + str(initialization_data["material_flow_percent"])+' ; set extrude factor override percentage'))
    if initialization_data['z_offset'] is not None:
        starting_procedure_steps.append(ManualGcode(text='SET_GCODE_OFFSET Z=' + str(initialization_data['z_offset']) + ' MOVE=1'))
    if initialization_data['include_purge']:
        starting_procedure_steps.append(Extruder(on=False))
        starting_procedure_steps.append(Point(x=5, y=5, z=10))
        starting_procedure_steps.append(StationaryExtrusion(volume=50, speed=250))
        starting_procedure_steps.append(Printer(travel_speed=250))
        starting_procedure_steps.append(Point(z=50))
        starting_procedure_steps.append(Printer(travel_speed=initialization_data["travel_speed"]))
        starting_procedure_steps.append(Point(x=10.0, y=10.0, z=0.3))
    starting_procedure_steps.append(Extruder(on=True))
    starting_procedure_steps.append(ManualGcode(text=';-----\n; END OF STARTING PROCEDURE\n;-----\n'))

    ending_procedure_steps = []
    ending_procedure_steps.append(ManualGcode(text='\n;-----\n; START OF ENDING PROCEDURE\n;-----'))
    ending_procedure_steps.append(ManualGcode(text='print_end    ;end script from macro\n; this final gcode line helps ensure the print_end macro is executed'))

    initialization_data['starting_procedure_steps'] = starting_procedure_steps
    initialization_data['ending_procedure_steps'] = ending_procedure_steps

    return initialization_data
