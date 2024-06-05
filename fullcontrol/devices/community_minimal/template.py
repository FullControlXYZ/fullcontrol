default_initial_settings = {
    # copy this file into the settings directory, edit it, then update library.json with an extra line for "printer_name_in_this_file: this_filename"
    "name": "Printer Name",
    # use curly braces to write expressions that should be evaluated
    # start or end gcode can cross reference settings in base_settings.py, this file, or any supplied as initialization_data in a GcodeControls object sent to fc.transform()
    "start_gcode": """
; ---- Starting gcode string:
M106 S{int(0.75*255)} ; 75% fan speed
M109 S{data['nozzle_temp']}
""",
    "end_gcode": ";---- Ending gcode string:\nM106 S0",
    # you can add any other settings from base_settings.py here
    # any settings defined here will override those in base_settings.py
    # you can also add new settings that aren't in base_settings.py but you might want to refer to in your start or end gcode and allow the user to override them with initialization_data in GcodeControls
    # any settings defined in a GcodeControls object fed to fc.transform() will override those in this file and base_settings.py
}
