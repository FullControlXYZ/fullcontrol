default_initial_settings = {
    "name": "Vivedino T-REX 2+",
    "manufacturer": "Vivedino, Formbot",
    "start_gcode": "T0\nG28 ; home all axes\nM420 S1\nG1 X-42 F8000\nG92 E0\nG1 E5 F500\nG1 X0 F5000\nG1 X-40\nG1 X0\nG1 X-40\nG1 X0\nG1 X-40\nG1 X200\nG1 Y200 F5000",
    "end_gcode": "G28 X0 Y0\nM104 S0 T1 ; turn off extruder\nM104 S0 T0\nM140 S0 ; turn off bed\nG28 X0\nM106 P0 S0\nM106 P1 S0\nM84 S0\nM84 XYE; disable motors except Z",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 100,
    "print_speed": 50.0,
    "travel_speed": 150.0,
    "dia_feed": 1.75,
    "build_volume_x": 400,
    "build_volume_y": 400,
    "build_volume_z": 500,
}