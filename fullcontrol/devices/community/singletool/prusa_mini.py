from fullcontrol.gcode import Point, Printer, Extruder, ManualGcode, PrinterCommand, GcodeComment, Buildplate, Hotend, Fan, StationaryExtrusion
import fullcontrol.devices.community.singletool.base_settings as base_settings


def set_up(user_overrides: dict):
    ''' DO THIS
    '''

    # overrides for this specific printer relative those defined in base_settings.py
    printer_overrides = {'primer': 'no_primer', "nozzle_probe_temp": 170}
    # update default initialization settings with printer-specific overrides and user-defined overrides
    initialization_data = {**base_settings.default_initial_settings, **printer_overrides}
    initialization_data = {**initialization_data, **user_overrides}

    starting_procedure_steps = []
    starting_procedure_steps.append(ManualGcode(
        text='; Time to print!!!!!\n; GCode created with FullControl - tell us what you\'re printing!\n; info@fullcontrol.xyz or tag FullControlXYZ on Twitter/Instagram/LinkedIn/Reddit/TikTok \n'))
    starting_procedure_steps.append(Buildplate(temp=initialization_data["bed_temp"], wait=False))
    # Prusa Mk3.9/Mk4 probe with a load cell, the official PrusaSlicer profiles
    # do this at 170 C (for PLA) to prevent oozing.
    starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_probe_temp"], wait=False))
    starting_procedure_steps.append(Buildplate(temp=initialization_data["bed_temp"], wait=True))
    starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_probe_temp"], wait=True))

    # For Prusa Mk3.9/Mk4 we perform mesh bed leveling once up to bed temp and
    # with nozzle at probing temp.
    starting_procedure_steps.append(PrinterCommand(id='home'))
    starting_procedure_steps.append(ManualGcode(text='G29 ; mesh bed leveling'))

    starting_procedure_steps.append(PrinterCommand(id='absolute_coords'))
    starting_procedure_steps.append(PrinterCommand(id='units_mm'))
    starting_procedure_steps.append(Extruder(relative_gcode=initialization_data["relative_e"]))

    starting_procedure_steps.append(Extruder(on=False))
    starting_procedure_steps.append(Point(x=5, y=5, z=10))

    starting_procedure_steps.append(ManualGcode(
        text='M220 S' + str(initialization_data["print_speed_percent"])+' ; set speed factor override percentage'))
    starting_procedure_steps.append(ManualGcode(
        text='M221 S' + str(initialization_data["material_flow_percent"])+' ; set extrude factor override percentage'))

    # Now go to target nozzle temperature, after we probed the bed and moved away from it
    starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_temp"], wait=True))

    starting_procedure_steps.append(Fan(speed_percent=initialization_data["fan_percent"]))
    starting_procedure_steps.append(ManualGcode(text='; intro line\n'))
    starting_procedure_steps.append(ManualGcode(text='; intro line\n'))
    starting_procedure_steps.append(ManualGcode(text='G1 X10 Z0.2 F1000\n'))
    starting_procedure_steps.append(ManualGcode(text='G1 X70 E8 F900\n'))
    starting_procedure_steps.append(ManualGcode(text='G1 X140 E10 F700\n'))
    starting_procedure_steps.append(ManualGcode(text='G92 E0\n'))

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
    ending_procedure_steps.append(ManualGcode(text='M221 S100 ; reset flow'))
    ending_procedure_steps.append(ManualGcode(text='M572 S0 ; reset PA'))
    ending_procedure_steps.append(ManualGcode(text='M593 X T2 F0 ; disable IS'))
    ending_procedure_steps.append(ManualGcode(text='M593 Y T2 F0 ; disable IS'))
    ending_procedure_steps.append(ManualGcode(text='M84 ; disable steppers'))

    initialization_data['starting_procedure_steps'] = starting_procedure_steps
    initialization_data['ending_procedure_steps'] = ending_procedure_steps

    return initialization_data
