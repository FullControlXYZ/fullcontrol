from fullcontrol.gcode import Point, Printer, Extruder, ManualGcode, PrinterCommand, Buildplate, Hotend, Fan, StationaryExtrusion
import fullcontrol.devices.community.singletool.base_settings as base_settings


def set_up(user_overrides: dict):
    ''' DO THIS
    '''

    # overrides for this specific printer relative those defined in base_settings.py
    printer_overrides = {'primer': 'no_primer', 'relative_e': False}
    # update default initialization settings with printer-specific overrides and user-defined overrides
    initialization_data = {**base_settings.default_initial_settings, **printer_overrides}
    initialization_data = {**initialization_data, **user_overrides}

    starting_procedure_steps = []
    starting_procedure_steps.append(ManualGcode(
        text='; Time to print!!!!!\n; GCode created with FullControl - tell us what you\'re printing!\n; info@fullcontrol.xyz or tag FullControlXYZ on Twitter/Instagram/LinkedIn/Reddit/TikTok'))
    if 'relative_e' in user_overrides.keys():
        starting_procedure_steps.append(Extruder(relative_gcode=initialization_data["relative_e"]))
    if 'bed_temp' in user_overrides.keys():
        starting_procedure_steps.append(Buildplate(temp=initialization_data["bed_temp"], wait=False))
    if 'nozzle_temp' in user_overrides.keys():
        starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_temp"], wait=False))
    if 'bed_temp' in user_overrides.keys():
        starting_procedure_steps.append(Buildplate(temp=initialization_data["bed_temp"], wait=True))
    if 'nozzle_temp' in user_overrides.keys():
        starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_temp"], wait=True))
    if 'fan_percent' in user_overrides.keys():
        starting_procedure_steps.append(Fan(speed_percent=initialization_data["fan_percent"]))
    if 'print_speed_percent' in user_overrides.keys():
        starting_procedure_steps.append(ManualGcode(
            text='M220 S' + str(initialization_data["print_speed_percent"])+' ; set speed factor override percentage'))
    if 'material_flow_percent' in user_overrides.keys():
        starting_procedure_steps.append(ManualGcode(
            text='M221 S' + str(initialization_data["material_flow_percent"])+' ; set extrude factor override percentage'))

    ending_procedure_steps = []

    initialization_data['starting_procedure_steps'] = starting_procedure_steps
    initialization_data['ending_procedure_steps'] = ending_procedure_steps

    return initialization_data
