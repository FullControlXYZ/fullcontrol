default_initial_settings = {
    "name": "Ultimaker 2",
    "manufacturer": "Ultimaker B.V.",
    "start_gcode": "G0 F3000 Y50 ;avoid prime blob",
    "end_gcode": ";Version _2.6 of the firmware can abort the print too early if the file ends\n;too soon. However if the file hasn't ended yet because there are comments at\n;the end of the file, it won't abort yet. Therefore we have to put at least 512\n;bytes at the end of the g-code so that the file is not yet finished by the\n;time that the motion planner gets flushed. With firmware version _3.3 this\n;should be fixed, so this comment wouldn't be necessary any more. Now we have\n;to pad this text to make precisely 512 bytes.",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 100,
    "print_speed": 60,
    "travel_speed": 120,
    "dia_feed": 2.85,
    "build_volume_x": 223,
    "build_volume_y": 223,
    "build_volume_z": 205,
}
