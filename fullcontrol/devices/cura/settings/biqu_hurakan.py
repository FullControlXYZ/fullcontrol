default_initial_settings = {
    "name": "Biqu Hurakan",
    "manufacturer": "Biqu",
    "start_gcode": ";BIQU Hurakan start code. Much complex. Very wow. Klipper FTW.\n\nSTART_PRINT BED_TEMP={data['bed_temp']} EXTRUDER_TEMP={data['nozzle_temp']}\n\n; Note: This start/end code is designed to work\n; with the stock cfg files provided  with the \n; BIQU Hurakan. If you alter the macros in the \n; cfg files then you may also need to alter this code.\n\n; Another note: This profile will get you \n; part of the way to good prints.\n; You still need to tweak settings for each \n; different filament that you use.\n; Settings such as retraction distance/speed, \n; flow, pressure advance, bed/nozzle temperatures\n; and others may need to be adjusted.\n; Use https://teachingtechyt.github.io/calibration.html to calibrate.\n; Also see https://www.youtube.com/watch?v=Ae2G7hl_pZc\n; for some good tips.",
    "end_gcode": ";BIQU Hurakan end code. More complex. Such wow. Klipper4Life.\n\nEND_PRINT",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 100,
    "print_speed": 120,
    "travel_speed": 200,
    "dia_feed": 1.75,
    "build_volume_x": 235,
    "build_volume_y": 235,
    "build_volume_z": 270,
}
