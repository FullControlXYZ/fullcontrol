default_initial_settings = {
    "name": "Robo 3D R1",
    "manufacturer": "Robo 3D",
    "start_gcode": " G92 E0 ;\n M565 Z-1 ;\n G1 Z5 F5000 ;\n G29 ;\n",
    "end_gcode": " M104 S0                     ;extruder heater off\n M140 S0                     ;heated bed heater off (if you have it)\n G91                                    ;relative positioning\n G1 E-1 F300                            ;retract the filament a bit before lifting the nozzle, to release some of the pressure\n G1 Z+0.5 E-5 X-20 Y-20 F{data['travel_speed']} ;move Z up a bit and retract filament even more\n G28 X0 Y0                              ;move X/Y to min endstops, so the head is out of the way\n M84                         ;steppers off\n G90                         ;absolute positioning\n",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 100,
    "print_speed": 40,
    "travel_speed": 120,
    "dia_feed": 2.85,
    "build_volume_x": 225,
    "build_volume_y": 245,
    "build_volume_z": 210,
}