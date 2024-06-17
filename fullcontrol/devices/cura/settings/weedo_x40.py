default_initial_settings = {
    "name": "Weedo X40",
    "manufacturer": "Weedo",
    "start_gcode": "; x40-community.org configuration Rev. 08\n;(**** start.gcode for WEEDO X40 DUAL****)\nT{data['extruder_number']} S ; Selected start extruder\nM140 S{data['bed_temp']} ; Preheat bed\nM109 S{data['nozzle_temp']}; Preheat nozzle\nM73 P0 ; Set current print progress percentage\nG21 ; Millimeter Units\nG90 ; Absolute positioning\nM82 ; Extruder in absolute mode\nT0 S ; Select left extruder\nM301 H1 P15.53 I1.32 D45.75 ; PID left extruder with Weedo X40 coolingsystem\n;M301 H1 P13.32 I0.98 D45.13 ; PID left extruder with X40 Community coolingsystem\nM92 E94.90 ; Calibrate left extruder\nT1 S ; Select right extruder\nM301 H1 P15.44 I1.29 D46.11 ; PID right extruder with Weedo X40 coolingsystem\n;M301 H1 P13.32 I0.98 D45.13 ; PID right extruder with X40 Community coolingsystem\nM92 E94.90 ; Calibrate right extruder\nT0 S ; Select left extruder\nG28 ; Auto home\nG29 ; Bed Leveling\nG1 X-47 F3000 ; Move left nozzle to parking position\nT1 S ; select right extruder\nG1 X351 F3000 ; Move right nozzle to parking position\nM107 P0 ; Turn off left fan\nM107 P1 ; Turn off right fan\nT{data['extruder_number']} S ; Set start extruder\nM190 S{data['bed_temp']} ; Waiting for bed temperature\nG1 E50 F100 ; Extrude in parking position\nM77 ; Stop heat up timer\nM75 ; Start print timer\n",
    "end_gcode": "(*********end X40 End.gcode*******)\nG28 X Y F3000\nG91 ; Relative positioning\nG1 E-6 ; Reduce filament pressure\nG90 ; Absolute positioning\nG0 Y300 F3000 ; Move headbed\nM104 S0 T0 ; Cool down left extruder\nM104 S0 T1 ; Cool down right extruder\nM140 S0 ; Cool down heatbed\nM107 P0 ; Turn off left fan\nM107 P1 ; Turn off right fan\nM82; Extruder in absolute mode\nM73 P100 ; Set print progress to 100%",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 100,
    "print_speed": 50.0,
    "travel_speed": 150,
    "dia_feed": 1.75,
    "build_volume_x": 300,
    "build_volume_y": 300,
    "build_volume_z": 400,
}