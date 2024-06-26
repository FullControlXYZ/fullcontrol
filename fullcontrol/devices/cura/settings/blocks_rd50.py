default_initial_settings = {
    "name": "Blocks RD50",
    "manufacturer": "Blocks",
    "start_gcode": "G21\nG90 ;absolute positioning\nG28 X0 Y0  ;move X/Y to min endstops\nG28 Z0 ;move Z to min endstops\n;PREHEAT\nM140 S{data['bed_temp']}   ; Set Heat Bed temperature\nM104 S{data['nozzle_temp']} ; Set Extruder temperature\nG1 X-60 Y0 F6000\nG92 E0       ;zero the extruded length\nM190 S{data['bed_temp']}   ; Wait for Heat Bed temperature\nM109 S{data['nozzle_temp']} ; Wait for Extruder temperature\nG1 F600 E20 ;extrude 10mm of feed stock\nG1 F200 E80 ;extrude 10mm of feed stock\nG12\nG92 E0       ;zero the extruded length again\nG29\nG1 Z0.2 F6000\nG1 F6000\n",
    "end_gcode": "M104 S0 ;extruder heater off\nM140 S0 ;heated bed heater off (if you have it)\nG91 ;relative positioning\nG1 E-1 F300 ;retract the filament a bit before lifting the nozzle, to release some of the pressure\nG1 Z+0.5 E-5 X-20 Y-20 F6000 ;move Z up a bit and retract filament even more\nG28 X0 Y0 ;move X/Y to min endstops, so the head is out of the way\nM84 ;steppers off\nG90 ;absolute positioning\n",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 100,
    "print_speed": 60,
    "travel_speed": 150.0,
    "dia_feed": 1.75,
    "build_volume_x": 500,
    "build_volume_y": 500,
    "build_volume_z": 500,
}
