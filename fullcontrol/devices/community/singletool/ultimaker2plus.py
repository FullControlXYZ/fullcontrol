from fullcontrol.gcode import Point, Printer, Extruder, ManualGcode, PrinterCommand, Buildplate, Hotend, Fan, StationaryExtrusion
import fullcontrol.devices.community.singletool.base_settings as base_settings


def set_up(user_overrides: dict):
    ''' DO THIS
    '''

    # overrides for this specific printer relative those defined in base_settings.py
    printer_overrides = {'e_units': 'mm3', 'dia_feed': 2.85}
    # update default initialization settings based on the printer-specific overrides and user-defined overrides
    initialization_data = {**base_settings.default_initial_settings, **printer_overrides}
    initialization_data = {**initialization_data, **user_overrides}

    starting_procedure_steps = []
    starting_procedure_steps.append(ManualGcode(text='\n;FLAVOR:UltiGCode\n;TIME:0\n;MATERIAL:1\n'))
    starting_procedure_steps.append(ManualGcode(
        text='; Time to print!!!!!\n; GCode created with FullControl - tell us what you\'re printing!\n; info@fullcontrol.xyz or tag FullControlXYZ on Twitter/Instagram/LinkedIn/Reddit/TikTok \n'))
    starting_procedure_steps.append(PrinterCommand(id='home'))
    starting_procedure_steps.append(Buildplate(temp=initialization_data["bed_temp"], wait=False))
    starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_temp"], wait=False))
    starting_procedure_steps.append(Buildplate(temp=initialization_data["bed_temp"], wait=True))
    starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_temp"], wait=True))
    starting_procedure_steps.append(PrinterCommand(id='absolute_coords'))
    starting_procedure_steps.append(PrinterCommand(id='units_mm'))
    starting_procedure_steps.append(Extruder(relative_gcode=initialization_data["relative_e"]))
    starting_procedure_steps.append(Fan(speed_percent=initialization_data["fan_percent"]))
    starting_procedure_steps.append(ManualGcode(
        text='M220 S' + str(initialization_data["print_speed_percent"])+' ; set speed factor override percentage'))
    starting_procedure_steps.append(ManualGcode(
        text='M221 S' + str(initialization_data["material_flow_percent"])+' ; set extrude factor override percentage'))
    starting_procedure_steps.append(Extruder(on=False))
    starting_procedure_steps.append(Point(x=5, y=5, z=10))
    starting_procedure_steps.append(Point(x=10.0, y=10.0, z=0.3))
    starting_procedure_steps.append(Extruder(on=True))
    starting_procedure_steps.append(ManualGcode(text=';-----\n; END OF STARTING PROCEDURE\n;-----\n'))

    ending_procedure_steps = []
    ending_procedure_steps.append(ManualGcode(text='\n;-----\n; START OF ENDING PROCEDURE\n;-----'))
    ending_procedure_steps.append(PrinterCommand(id='retract'))
    ending_procedure_steps.append(ManualGcode(text='G91 ; relative coordinates'))
    ending_procedure_steps.append(ManualGcode(text='G0 Z20 F8000 ; drop bed'))
    ending_procedure_steps.append(ManualGcode(text='G90 ; absolute coordinates'))
    ending_procedure_steps.append(Fan(speed_percent=0))
    ending_procedure_steps.append(Buildplate(temp=0, wait=False))
    ending_procedure_steps.append(Hotend(temp=0, wait=False))
    ending_procedure_steps.append(ManualGcode(text='M84 ; disable steppers'))
    ending_procedure_steps.append(ManualGcode(text='\n; This GCode is just padding because some printer firmwares need it'*25))

    initialization_data['starting_procedure_steps'] = starting_procedure_steps
    initialization_data['ending_procedure_steps'] = ending_procedure_steps

    return initialization_data
