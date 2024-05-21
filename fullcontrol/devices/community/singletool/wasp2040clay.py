from fullcontrol.gcode import Point, Printer, Extruder, ManualGcode, PrinterCommand, Buildplate, Hotend, Fan, StationaryExtrusion
import fullcontrol.devices.community.singletool.base_settings as base_settings


def set_up(user_overrides: dict):
    ''' DO THIS
    '''

    # overrides for this specific printer relative those defined in base_settings.py
    printer_overrides = {
        "extrusion_width": 1.2,
        "extrusion_height": 0.6,
        "dia_feed": 3.1,  # dia_feed was manual chosen based on measured extrusion volumes to achieve the correct E value in gcode. in the future it would be good if the used can directly define the relationship between volume and E rather than hacking dia_feed
        "travel_speed": 4000,
        "travel_format": "G1_E0",
        'primer': 'travel'}
    # update default initialization settings with printer-specific overrides and user-defined overrides
    initialization_data = {**base_settings.default_initial_settings, **printer_overrides}
    initialization_data = {**initialization_data, **user_overrides}

    starting_procedure_steps = []
    starting_procedure_steps.append(ManualGcode(
        text='; Time to print!!!!!\n; GCode created with FullControl - tell us what you\'re printing!\n; info@fullcontrol.xyz or tag FullControlXYZ on Twitter/Instagram/LinkedIn/Reddit/TikTok \n'))
    starting_procedure_steps.append(PrinterCommand(id='units_mm'))
    starting_procedure_steps.append(PrinterCommand(id='home'))
    starting_procedure_steps.append(PrinterCommand(id='absolute_coords'))
    starting_procedure_steps.append(Extruder(relative_gcode=initialization_data["relative_e"]))
    starting_procedure_steps.append(ManualGcode(
        text='M220 S' + str(initialization_data["print_speed_percent"])+' ; set speed factor override percentage'))
    starting_procedure_steps.append(ManualGcode(
        text='M221 S' + str(initialization_data["material_flow_percent"])+' ; set extrude factor override percentage'))
    starting_procedure_steps.append(Extruder(on=False))
    starting_procedure_steps.append(Point(x=0, y=-90, z=50))
    starting_procedure_steps.append(StationaryExtrusion(volume=300, speed=120))
    starting_procedure_steps.append(Printer(travel_speed=250))
    starting_procedure_steps.append(Point(z=100))
    starting_procedure_steps.append(Printer(travel_speed=initialization_data["travel_speed"]))
    starting_procedure_steps.append(Extruder(on=True))
    starting_procedure_steps.append(ManualGcode(text=';-----\n; END OF STARTING PROCEDURE\n;-----\n'))

    ending_procedure_steps = []
    ending_procedure_steps.append(ManualGcode(text='\n;-----\n; START OF ENDING PROCEDURE\n;-----'))
    ending_procedure_steps.append(PrinterCommand(id='home'))

    initialization_data['starting_procedure_steps'] = starting_procedure_steps
    initialization_data['ending_procedure_steps'] = ending_procedure_steps

    return initialization_data
