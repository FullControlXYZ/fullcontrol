default_initial_settings = {
    "print_speed": 1000,
    "travel_speed": 8000,
    "area_model": "rectangle",
    "extrusion_width": 0.4,
    "extrusion_height": 0.2,
    "nozzle_temp": 210,
    "bed_temp": 40,
    "fan_percent": 100,
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
        "relative_coords": "G91 ; absolute coordinates",
        "units_mm": "G21 ; set units to millimeters"
    }
}
