default_initial_settings = {
    "name": "Flsun Q5",
    "manufacturer": "Flsun",
    "start_gcode": ";FLAVOR:Marlin\nM82 ;absolute extrusion mode\nG21\nG90\nM82\nM107 T0\nG28\nG92 E0\nG0 E3 F200\nG92 E0 ; reset extrusion distance\nM106 S255 ; Enable cooling fan full speed\nG1 X-98 Y0 Z0.4 F3000 ; move to arc start\nG3 X0 Y-98 I98 Z0.4 E40 F400 ; lay arc stripe 90deg\nG92 E0 ; reset extrusion distance\nG4 P500 ; wait for 0.5 sec\nG0 Z10 E-1 ; Lift 15mm and retract 1mm filament\nG4 P2000 ; wait for 5 sec\nG0 Z15\nM107 ; Disable cooling fan\nG1 X0 Y-85 Z4 E0 F3000 ; get off the bed",
    "end_gcode": "M104 S0\nM140 S0\nG92 E1\nG1 E-1 F300\nG28 X0 Y0\nM84\nM82 ;absolute extrusion mode\nM104 S0",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 100,
    "print_speed": 60,
    "travel_speed": 120,
    "dia_feed": 2.85,
    "build_volume_x": 200,
    "build_volume_y": 200,
    "build_volume_z": 200,
}
