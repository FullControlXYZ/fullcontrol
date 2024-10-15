from fullcontrol.gcode import Point, Printer, Extruder, ManualGcode, PrinterCommand, GcodeComment, Buildplate, Hotend, Fan, StationaryExtrusion
import fullcontrol.devices.community.singletool.base_settings as base_settings


def set_up(user_overrides: dict):
    ''' DO THIS
    '''

    # overrides for this specific printer relative those defined in base_settings.py
    printer_overrides = {
        "model_height": 250,
        "bed_type": "Textured PEI Plate",
        "print_speed": 1000,
        "travel_speed": 8000,
        "area_model": "rectangle",
        "extrusion_width": 0.4,
        "extrusion_height": 0.2,
        "nozzle_temp": 220,
        "bed_temp": 55,
        "parts_fan_percent": 50,
        "aux_fan_percent": 0,
        "chamber_fan_percent":30,
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

    model_height = initialization_data["model_height"]

    # STARTING PROCEDURE

    starting_procedure_steps = []
    starting_procedure_steps.append(ManualGcode(
        text='; Time to print!!!!!\n; GCode created with FullControl - tell us what you\'re printing!\n; info@fullcontrol.xyz or tag FullControlXYZ on Twitter/Instagram/LinkedIn/Reddit/TikTok \n'))
    starting_procedure_steps.append(ManualGcode(
        text='; For BambuLab P1 Printers, when using custom GCode, the first print after start-up may stop extruding shortly after starting. Just re-print\n'))

    # printer resets
    starting_procedure_steps.append(ManualGcode(text='\n;--- printer reset ---\n'))
    starting_procedure_steps.append(PrinterCommand(id='relative_coords'))
    starting_procedure_steps.append(ManualGcode(text='M17 Z0.4 ; lower the z-motor current'))
    starting_procedure_steps.append(ManualGcode(text='G380 S2 Z30 F300 ; G380 is same as G38; lower the hotbed , to prevent the nozzle is below the hotbed'))
    starting_procedure_steps.append(ManualGcode(text='G380 S2 Z-25 F300 ;'))
    starting_procedure_steps.append(ManualGcode(text='G1 Z5 F300 ;'))
    starting_procedure_steps.append(ManualGcode(text='M17 X1.2 Y1.2 Z0.75 ; reset motor current to default'))
    starting_procedure_steps.append(PrinterCommand(id='absolute_coords'))
    starting_procedure_steps.append(ManualGcode(text='M220 S100 ; Reset Feedrate'))
    starting_procedure_steps.append(ManualGcode(text='M221 S100 ; Reset Flowrate'))
    starting_procedure_steps.append(ManualGcode(text='M73.2 R1.0 ; Reset left time magnitude'))
    starting_procedure_steps.append(ManualGcode(text='M221 X0 Y0 Z0 ; turn off soft endstop to prevent protential logic problem'))
    starting_procedure_steps.append(ManualGcode(text='G29.1 Z0.0 ; clear z-trim value first'))
    starting_procedure_steps.append(ManualGcode(text='M204 S10000 ; init ACC set to 10m/s^2'))

    # start bed heating and toolhead heating
    starting_procedure_steps.append(ManualGcode(text='\n;--- heat build plate ---\n'))
    starting_procedure_steps.append(Buildplate(temp=initialization_data["bed_temp"], wait=False))
    starting_procedure_steps.append(ManualGcode(text='M106 P2 S100 ; turn on aux fan to cool toolhead'))
    starting_procedure_steps.append(Hotend(temp=250, wait=False))
    starting_procedure_steps.append(Extruder(on=False))

    # prepare print temperature and material
    starting_procedure_steps.append(ManualGcode(text='\n;--- prepare toolhead ---\n'))
    starting_procedure_steps.append(PrinterCommand(id='relative_coords'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z10 F1200'))
    starting_procedure_steps.append(PrinterCommand(id='absolute_coords'))
    starting_procedure_steps.append(ManualGcode(text='G28 X Y'))
    starting_procedure_steps.append(ManualGcode(text='M975 S1 ; turn on vibration suppression'))
    starting_procedure_steps.append(ManualGcode(text='G1 X60 F12000'))
    starting_procedure_steps.append(ManualGcode(text='G1 Y245'))
    starting_procedure_steps.append(ManualGcode(text='G1 Y265 F3000'))
    
    # purge filament
    starting_procedure_steps.append(ManualGcode(text='\n;--- purge filament ---\n'))
    starting_procedure_steps.append(ManualGcode(text='M412 S1 ; turn on filament runout detection'))
    starting_procedure_steps.append(Hotend(temp=250, wait=True))
    starting_procedure_steps.append(Fan(speed_percent=0))
    starting_procedure_steps.append(ManualGcode(text='G92 E0'))
    starting_procedure_steps.append(StationaryExtrusion(volume=50, speed=200))
    starting_procedure_steps.append(ManualGcode(text='M400 ; wait for buffer to clear'))
    starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_temp"], wait=False))
    starting_procedure_steps.append(ManualGcode(text='G92 E0'))
    starting_procedure_steps.append(StationaryExtrusion(volume=50, speed=200))
    starting_procedure_steps.append(ManualGcode(text='M400 ; wait for buffer to clear'))
    starting_procedure_steps.append(Fan(speed_percent=100))
    starting_procedure_steps.append(ManualGcode(text='G92 E0'))
    starting_procedure_steps.append(StationaryExtrusion(volume=20, speed=300))
    starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_temp"] - 20, wait=True))
    starting_procedure_steps.append(ManualGcode(text=' ; drop nozzle temp, make filament shrink a bit'))
    starting_procedure_steps.append(ManualGcode(text='G92 E0'))
    starting_procedure_steps.append(ManualGcode(text='G1 E-.5 F300'))

    # nozzle wipe
    starting_procedure_steps.append(ManualGcode(text='\n;--- nozzle wipe ---\n'))
    starting_procedure_steps.append(ManualGcode(text='G1 X70 F9000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X76 F15000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X65 F15000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X76 F15000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X65 F15000 ; shake to put down garbage'))
    starting_procedure_steps.append(ManualGcode(text='G1 X80 F6000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X95 F15000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X80 F15000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X165 F15000 ; wipe and shake'))
    starting_procedure_steps.append(ManualGcode(text='M400 ; wait for buffer to clear'))
    starting_procedure_steps.append(ManualGcode(text='G92 E0'))
    starting_procedure_steps.append(ManualGcode(text='G1 E-.5 F300'))
    starting_procedure_steps.append(Fan(speed_percent=0))

    # clean nozzle procedure
    starting_procedure_steps.append(ManualGcode(text='\n;--- clean nozzle ---\n'))
    starting_procedure_steps.append(ManualGcode(text='M975 S1 ; turn on vibration suppression'))
    starting_procedure_steps.append(Fan(speed_percent=100))
    starting_procedure_steps.append(ManualGcode(text='G1 X65 Y230 F18000'))
    starting_procedure_steps.append(ManualGcode(text='G1 Y264 F6000'))
    starting_procedure_steps.append(Hotend(temp=140, wait=False))
    starting_procedure_steps.append(ManualGcode(text='G1 X100 F18000 ; first wipe mouth'))

    starting_procedure_steps.append(ManualGcode(text='G0 X135 Y253 F20000 ; move to exposed steel surface edge'))
    starting_procedure_steps.append(ManualGcode(text='G28 Z P0 T300 ; home z with low precision, permit 300deg temperature'))
    starting_procedure_steps.append(ManualGcode(text='G29.2 S0 ; turn off ABL'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z5 F20000'))

    starting_procedure_steps.append(ManualGcode(text='G1 X60 Y265'))
    starting_procedure_steps.append(ManualGcode(text='G92 E0'))
    starting_procedure_steps.append(ManualGcode(text='G1 E-0.5 F300 ; retrack more'))
    starting_procedure_steps.append(ManualGcode(text='G1 X100 F5000 ; second wipe mouth'))
    starting_procedure_steps.append(ManualGcode(text='G1 X70 F15000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X100 F5000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X70 F15000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X100 F5000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X70 F15000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X100 F5000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X70 F15000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X90 F5000'))
    starting_procedure_steps.append(ManualGcode(text='G0 X128 Y261 Z-1.5 F20000 ; move to exposed steel surface and stop the nozzle'))
    starting_procedure_steps.append(Hotend(temp=140, wait=True))
    starting_procedure_steps.append(Fan(speed_percent=100))

    starting_procedure_steps.append(ManualGcode(text='M221 S ; push soft endstop status'))
    starting_procedure_steps.append(ManualGcode(text='M221 Z0 ; turn off Z axis endstop'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z0.5 F20000'))
    starting_procedure_steps.append(ManualGcode(text='G0 X125 Y259.5 Z-1.01'))
    starting_procedure_steps.append(ManualGcode(text='G0 X131 F211'))
    starting_procedure_steps.append(ManualGcode(text='G0 X124'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z0.5 F20000'))
    starting_procedure_steps.append(ManualGcode(text='G0 X125 Y262.5'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z-1.01'))
    starting_procedure_steps.append(ManualGcode(text='G0 X131 F211'))
    starting_procedure_steps.append(ManualGcode(text='G0 X124'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z0.5 F20000'))
    starting_procedure_steps.append(ManualGcode(text='G0 X125 Y260.0'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z-1.01'))
    starting_procedure_steps.append(ManualGcode(text='G0 X131 F211'))
    starting_procedure_steps.append(ManualGcode(text='G0 X124'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z0.5 F20000'))
    starting_procedure_steps.append(ManualGcode(text='G0 X125 Y262.0'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z-1.01'))
    starting_procedure_steps.append(ManualGcode(text='G0 X131 F211'))
    starting_procedure_steps.append(ManualGcode(text='G0 X124'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z0.5 F20000'))
    starting_procedure_steps.append(ManualGcode(text='G0 X125 Y260.5'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z-1.01'))
    starting_procedure_steps.append(ManualGcode(text='G0 X131 F211'))
    starting_procedure_steps.append(ManualGcode(text='G0 X124'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z0.5 F20000'))
    starting_procedure_steps.append(ManualGcode(text='G0 X125 Y261.5'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z-1.01'))
    starting_procedure_steps.append(ManualGcode(text='G0 X131 F211'))
    starting_procedure_steps.append(ManualGcode(text='G0 X124'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z0.5 F20000'))
    starting_procedure_steps.append(ManualGcode(text='G0 X125 Y261.0'))
    starting_procedure_steps.append(ManualGcode(text='G0 Z-1.01'))
    starting_procedure_steps.append(ManualGcode(text='G0 X131 F211'))
    starting_procedure_steps.append(ManualGcode(text='G0 X124'))
    starting_procedure_steps.append(ManualGcode(text='G0 X128'))
    starting_procedure_steps.append(ManualGcode(text='G2 I0.5 J0 F300'))
    starting_procedure_steps.append(ManualGcode(text='G2 I0.5 J0 F300'))
    starting_procedure_steps.append(ManualGcode(text='G2 I0.5 J0 F300'))
    starting_procedure_steps.append(ManualGcode(text='G2 I0.5 J0 F300'))

    starting_procedure_steps.append(ManualGcode(text='G2 I0.5 J0 F3000'))
    starting_procedure_steps.append(ManualGcode(text='G2 I0.5 J0 F3000'))
    starting_procedure_steps.append(ManualGcode(text='G2 I0.5 J0 F3000'))
    starting_procedure_steps.append(ManualGcode(text='G2 I0.5 J0 F3000'))

    # starting_procedure_steps.append(ManualGcode(text='M221 Z1 ; turn on Z endstop'))
    starting_procedure_steps.append(ManualGcode(text='M221 R ; pop soft endstop status'))
    starting_procedure_steps.append(ManualGcode(text='G1 Z10 F1200'))
    starting_procedure_steps.append(ManualGcode(text='M400 ; wait for buffer to clear'))
    starting_procedure_steps.append(ManualGcode(text='G1 Z10'))
    starting_procedure_steps.append(ManualGcode(text='G1 F30000'))
    starting_procedure_steps.append(ManualGcode(text='G1 X230 Y15'))
    starting_procedure_steps.append(ManualGcode(text='G29.2 S1 ; turn on ABL'))
    starting_procedure_steps.append(Fan(speed_percent=0))
    
    # home toolhead
    starting_procedure_steps.append(ManualGcode(text='\n;--- home toolhead ---\n'))
    starting_procedure_steps.append(PrinterCommand(id='home'))
    starting_procedure_steps.append(PrinterCommand(id='absolute_coords'))
    starting_procedure_steps.append(PrinterCommand(id='units_mm'))
    starting_procedure_steps.append(Extruder(relative_gcode=initialization_data["relative_e"]))
    starting_procedure_steps.append(Point(x=20, y=20, z=10))
    starting_procedure_steps.append(ManualGcode(text='G92 X0 Y0 ; offset print to avoid filament cutting area'))
    starting_procedure_steps.append(Point(x=5, y=5, z=10))

    # set hotend temperature
    starting_procedure_steps.append(ManualGcode(text='\n;--- wait for bed temperature and set hot end temperature ---\n'))
    starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_temp"], wait=True))
    starting_procedure_steps.append(Buildplate(temp=initialization_data["bed_temp"], wait=True))

    # lower bed for PEI plate
    if initialization_data["bed_type"] == "Textured PEI Plate":
        starting_procedure_steps.append(ManualGcode(text='\n;--- lower bed for PEI plate ---\n'))
        starting_procedure_steps.append(ManualGcode(text='G29.1 Z-0.04 ; for Textured PEI Plate'))

    # wait for extrude temperature, set fan and travel speed
    starting_procedure_steps.append(ManualGcode(text='\n;--- wait for hot end temperature ---\n'))
    starting_procedure_steps.append(Fan(speed_percent=initialization_data["parts_fan_percent"]))
    starting_procedure_steps.append(ManualGcode(text=f'M106 P2 S{int(initialization_data["aux_fan_percent"] / 100 * 255)} ; enable aux fan'))
    starting_procedure_steps.append(ManualGcode(text=f'M106 P3 S{int(initialization_data["chamber_fan_percent"] / 100 * 255)} ; enable chamber fan'))
    starting_procedure_steps.append(ManualGcode(text='M975 S1 ; turn on vibration suppression'))
    starting_procedure_steps.append(Printer(travel_speed=initialization_data["travel_speed"]))
    starting_procedure_steps.append(Point(x=10.0, y=10.0, z=0.3))
    starting_procedure_steps.append(Extruder(on=True))

    # set print speed and material flow
    starting_procedure_steps.append(ManualGcode(text='\n;--- set print speed and flow ---\n'))
    starting_procedure_steps.append(ManualGcode(
        text='M220 S' + str(initialization_data["print_speed_percent"]) + ' ; set speed factor override percentage'))
    starting_procedure_steps.append(ManualGcode(
        text='M221 S' + str(initialization_data["material_flow_percent"]) + ' ; set extrude factor override percentage'))
    
    starting_procedure_steps.append(ManualGcode(text=';==========\n; END OF STARTING PROCEDURE\n;==========\n'))


    # ENDING PROCEDURE

    ending_procedure_steps = []
    ending_procedure_steps.append(ManualGcode(text='\n;==========\n; START OF ENDING PROCEDURE\n;==========\n'))
    
    # retract filament and drop bed
    ending_procedure_steps.append(ManualGcode(text='\n;--- drop build plate ---\n'))
    ending_procedure_steps.append(ManualGcode(text='M400 ; wait for buffer to clear'))
    ending_procedure_steps.append(ManualGcode(text='G92 E0 ; zero the extruder'))
    ending_procedure_steps.append(ManualGcode(text='G1 E-1.5 F1800 ; retract'))
    ending_procedure_steps.append(ManualGcode(text=f'G1 Z{model_height + 0.5} F900 ; drop bed a little'))

    # move toolhead
    ending_procedure_steps.append(ManualGcode(text='\n;--- move toolhead back ---\n'))
    ending_procedure_steps.append(ManualGcode(text='G28 X Y ; home the X and Y axes'))
    ending_procedure_steps.append(ManualGcode(text='G1 X65 F12000'))
    ending_procedure_steps.append(ManualGcode(text='G1 Y245'))
    ending_procedure_steps.append(ManualGcode(text='G1 Y265 F3000'))
    ending_procedure_steps.append(ManualGcode(text='G1 X65 Y245 F12000'))
    ending_procedure_steps.append(ManualGcode(text='G1 Y265 F3000'))
    
    # turn heat bed and fans off
    ending_procedure_steps.append(ManualGcode(text='\n;--- turn heat bed and fans off ---\n'))
    ending_procedure_steps.append(Buildplate(temp=0, wait=False))
    ending_procedure_steps.append(Fan(speed_percent=0))
    ending_procedure_steps.append(ManualGcode(text='M106 P2 S0 ; disable aux fan'))
    ending_procedure_steps.append(ManualGcode(text='M106 P3 S0 ; disable chamber fan'))
    ending_procedure_steps.append(ManualGcode(text='G1 X100 F12000 ; remove oozed filament'))

    # wipe
    ending_procedure_steps.append(ManualGcode(text='\n;--- wipe nozzle ---\n'))
    ending_procedure_steps.append(ManualGcode(text='G1 X65 F12000'))
    ending_procedure_steps.append(ManualGcode(text='G1 Y265'))
    ending_procedure_steps.append(ManualGcode(text='G1 X100 F12000 ; wipe'))

    # turn off hot end
    ending_procedure_steps.append(ManualGcode(text='\n;--- turn off hotend ---\n'))
    ending_procedure_steps.append(Hotend(temp=0, wait=False))

    # move bed down
    ending_procedure_steps.append(ManualGcode(text='\n;--- lower build plate ---\n'))
    ending_procedure_steps.append(ManualGcode(text='M400 ; wait for buffer to clear'))
    ending_procedure_steps.append(ManualGcode(text='M17 S'))
    ending_procedure_steps.append(ManualGcode(text='M17 Z0.4 ; lower z motor current to reduce impact if there is something in the bottom'))
    if (model_height + 1 + 50.0) < 250.0:
        ending_procedure_steps.append(ManualGcode(text=f'G1 Z{model_height + 50} F600'))
        ending_procedure_steps.append(ManualGcode(text=f'G1 Z{model_height + 48}'))
    else:
        ending_procedure_steps.append(ManualGcode(text='G1 Z250 F600'))
        ending_procedure_steps.append(ManualGcode(text='G1 Z248'))    
    ending_procedure_steps.append(ManualGcode(text='M400 P100'))
    ending_procedure_steps.append(ManualGcode(text='M17 R ; restore z current'))

    # park toolhead
    ending_procedure_steps.append(ManualGcode(text='\n;--- park toolhead ---\n'))
    ending_procedure_steps.append(PrinterCommand(id='absolute_coords'))
    ending_procedure_steps.append(ManualGcode(text='G1 X128 Y250 F3600'))
    
    # reset
    ending_procedure_steps.append(ManualGcode(text='\n;--- reset printer parameters ---\n'))
    ending_procedure_steps.append(ManualGcode(text='M221 S100 ; reset flow'))
    ending_procedure_steps.append(ManualGcode(text='M201.2 K1.0 ; Reset acc magnitude'))
    ending_procedure_steps.append(ManualGcode(text='M73.2 R1.0 ; Reset left time magnitude'))
    ending_procedure_steps.append(ManualGcode(text='M1002 set_gcode_claim_speed_level : 0'))
    ending_procedure_steps.append(ManualGcode(text='M900 K0 ; reset LA'))
    ending_procedure_steps.append(ManualGcode(text='M84 ; disable steppers'))

    ###

    initialization_data['starting_procedure_steps'] = starting_procedure_steps
    initialization_data['ending_procedure_steps'] = ending_procedure_steps

    return initialization_data
