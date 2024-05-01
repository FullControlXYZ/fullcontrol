from fullcontrol.gcode import Point, Printer, Extruder, ManualGcode, PrinterCommand, GcodeComment, Buildplate, Hotend, Fan, StationaryExtrusion
import fullcontrol.gcode.printer_library.singletool.base_settings as base_settings


def set_up(user_overrides: dict):
    ''' DO THIS
    '''

    # overrides for this specific printer relative those defined in base_settings.py
    printer_overrides = {
        "print_speed": 2000,
        "travel_speed": 5000,
        "area_model": "rectangle",
        "extrusion_width": 0.4,
        "extrusion_height": 0.2,
        "nozzle_temp": 220,
        "bed_temp": 55,
        "part_fan_percent": 40,
        "aux_fan_percent": 0,
        "chamber_fan_percent": 20,
        "print_speed_percent": 100,
        "material_flow_percent": 100,
        "e_units": "mm",  # options: "mm" / "mm3"
        "relative_e": True,
        "manual_e_ratio": None,
        "dia_feed": 1.75,
        "travel_format": "G0",  # options: "G0" / "G1_E0"
        "primer": "front_lines_then_y",
        "printer_command_list": {
            "home": "G28 ; home axes",
            "retract": "G10 ; retract",
            "unretract": "G11 ; unretract",
            "absolute_coords": "G90 ; absolute coordinates",
            "relative_coords": "G91 ; relative coordinates",
            "units_mm": "G21 ; set units to millimeters"
        }
    }
    # update default initialization settings with printer-specific overrides and user-defined overrides
    initialization_data = {**base_settings.default_initial_settings, **printer_overrides}
    initialization_data = {**initialization_data, **user_overrides}

    starting_procedure_steps = []
    starting_procedure_steps.append(ManualGcode(
        text='; Time to print!!!!!\n; GCode created with FullControl - tell us what you\'re printing!\n; info@fullcontrol.xyz or tag FullControlXYZ on Twitter/Instagram/LinkedIn/Reddit/TikTok \n'))
    starting_procedure_steps.append(ManualGcode(
        text='; For BambuLab P1 Printers, when using custom GCode, the first print after start-up may stop extruding shortly after starting. Just re-print\n'))
    starting_procedure_steps.append(Buildplate(temp=initialization_data["bed_temp"], wait=False))
    starting_procedure_steps.append(Hotend(temp=150, wait=False))
    starting_procedure_steps.append(Buildplate(temp=initialization_data["bed_temp"], wait=True))
    starting_procedure_steps.append(Hotend(temp=150, wait=True))
    # load filament from AMS
    
    # purge filament

    # wipe nozzle procedure

    # home toolhead
    starting_procedure_steps.append(PrinterCommand(id='home'))
    starting_procedure_steps.append(GcodeComment(end_of_previous_line_text=' ; including mesh bed level'))
    starting_procedure_steps.append(PrinterCommand(id='absolute_coords'))
    starting_procedure_steps.append(PrinterCommand(id='units_mm'))

    starting_procedure_steps.append(Extruder(relative_gcode=initialization_data["relative_e"]))
    starting_procedure_steps.append(Fan(speed_percent=initialization_data["fan_percent"]))
    
    starting_procedure_steps.append(ManualGcode(text='M106 P2 S255 ; enable aux fan'))
    starting_procedure_steps.append(Point(x=20, y=30, z=10)) # updated from (20, 20, 10) to (20, 30, 10)
    starting_procedure_steps.append(ManualGcode(text='G92 X0 Y0 ; offset print to avoid filament cutting area'))
    starting_procedure_steps.append(Point(x=5, y=5, z=10))
    starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_temp"], wait=True))
    starting_procedure_steps.append(Extruder(on=False))
    starting_procedure_steps.append(StationaryExtrusion(volume=50, speed=250))
    starting_procedure_steps.append(Printer(travel_speed=250))
    starting_procedure_steps.append(Point(z=50))
    starting_procedure_steps.append(Printer(travel_speed=initialization_data["travel_speed"]))
    starting_procedure_steps.append(Point(x=10.0, y=10.0, z=0.3))
    starting_procedure_steps.append(Extruder(on=True))
    starting_procedure_steps.append(ManualGcode(
        text='M220 S' + str(initialization_data["print_speed_percent"])+' ; set speed factor override percentage'))
    starting_procedure_steps.append(ManualGcode(
        text='M221 S' + str(initialization_data["material_flow_percent"])+' ; set extrude factor override percentage'))
    starting_procedure_steps.append(ManualGcode(text=';-----\n; END OF STARTING PROCEDURE\n;-----\n'))


    ending_procedure_steps = []
    ending_procedure_steps.append(ManualGcode(text='\n;-----\n; START OF ENDING PROCEDURE\n;-----'))
    ending_procedure_steps.append(ManualGcode(text='M400 ; wait for buffer to clear'))
    ending_procedure_steps.append(ManualGcode(text='M83\nG0 E-0.8 F1800 ; retract'))
    # move toolhead
    starting_procedure_steps.append(PrinterCommand(id='relative_coords'))
    ending_procedure_steps.append(ManualGcode(text='G0 Z1 F900 ; drop bed a little'))
    starting_procedure_steps.append(PrinterCommand(id='absolute_coords'))
    ending_procedure_steps.append(ManualGcode(text='G1 X65 Y245 F12000 ; move to safe position'))
    ending_procedure_steps.append(ManualGcode(text='G1 Y265 F3000'))
    ending_procedure_steps.append(ManualGcode(text='G1 X65 Y245 F12000'))
    ending_procedure_steps.append(ManualGcode(text='G1 Y265 F3000'))
    # turn everything heat bed and fans
    ending_procedure_steps.append(Buildplate(temp=0, wait=False))
    ending_procedure_steps.append(Fan(speed_percent=0))
    ending_procedure_steps.append(ManualGcode(text='M106 P2 S0 ; disable aux fan'))
    ending_procedure_steps.append(ManualGcode(text='M106 P3 S0 ; disable chamber fan'))
    # wipe
    ending_procedure_steps.append(ManualGcode(text='G1 X100 F12000 ; wipe'))
    ending_procedure_steps.append(ManualGcode(text='G1 X20 Y50 F12000'))
    ending_procedure_steps.append(ManualGcode(text='G1 Y-3'))
    ending_procedure_steps.append(ManualGcode(text='G1 X65 F12000'))
    ending_procedure_steps.append(ManualGcode(text='G1 Y265'))
    ending_procedure_steps.append(ManualGcode(text='G1 X100 F12000 ; wipe'))
    # turn off hot end
    ending_procedure_steps.append(Hotend(temp=0, wait=False))
    # move bed down
    ending_procedure_steps.append(ManualGcode(text='M400 ; wait for buffer to clear'))
    ending_procedure_steps.append(ManualGcode(text='M17 S'))
    ending_procedure_steps.append(ManualGcode(text='M17 Z0.4 ; lower z motor current to reduce impact if there is something in the bottom'))
    ending_procedure_steps.append(ManualGcode(text='{if (max_layer_z + 100.0) < 250}\nG1 Z{max_layer_z + 100.0} F600\nG1 Z{max_layer_z +98.0}\n{else}\nG1 Z250 F600\nG1 Z248\n{endif}'))
    ending_procedure_steps.append(ManualGcode(text='M400 P100'))
    ending_procedure_steps.append(ManualGcode(text='M17 R ; restore z current'))
    # park toolhead
    starting_procedure_steps.append(PrinterCommand(id='absolute_coords'))
    ending_procedure_steps.append(ManualGcode(text='G1 X128 Y250 F3600'))
    # reset
    ending_procedure_steps.append(ManualGcode(text='M221 S100 ; reset flow'))
    ending_procedure_steps.append(ManualGcode(text='M201.2 K1.0 ; Reset acc magnitude'))
    ending_procedure_steps.append(ManualGcode(text='M73.2 R1.0 ; Reset left time magnitude'))
    ending_procedure_steps.append(ManualGcode(text='M900 K0 ; reset LA'))
    ending_procedure_steps.append(ManualGcode(text='M84 ; disable steppers'))

    initialization_data['starting_procedure_steps'] = starting_procedure_steps
    initialization_data['ending_procedure_steps'] = ending_procedure_steps

    return initialization_data
