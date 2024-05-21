default_initial_settings = {
    "name": "Felix Pro 2 Dual",
    "manufacturer": "Felix",
    "start_gcode": "G90 ;absolute positioning\nM82 ;set extruder to absolute mode\nM107 ;start with the fan off\nG28 X0 Y0 ;move X/Y to min endstops\nG28 Z0 ;move Z to min endstops\nG1 Z15.0 F9000 ;move the platform down 15mm\n\nT0 ;Switch to the 1st extruder\nG92 E0 ;zero the extruded length\nG1 F200 E6 ;extrude 6 mm of feed stock\nG92 E0 ;zero the extruded length again\n;G1 F9000\nM117 FPro2 printing...\n",
    "end_gcode": "; Endcode FELIXprinters Pro series\n; =================================	; Move extruder to park position\nG91   					; Make coordinates relative\nG1 Z2 F5000   				; Move z 2mm up\nG90   					; Use absolute coordinates again		\nG1 X220 Y243 F7800 			; Move bed and printhead to ergonomic position\n\n; =================================	; Turn off heaters\nT0					; Select left extruder\nM104 T0 S0				; Turn off heater and continue				\nG92 E0					; Reset extruder position\nG1 E-8					; Retract filament 8mm\nG1 E-5					; Push back filament 3mm\nG92 E0					; Reset extruder position\n\nT1					; Select right extruder\nM104 T1 S0				; Turn off heater and continu\nG92 E0					; Reset extruder position\nG1 E-8					; Retract filament 8mm\nG1 E-5					; Push back filament 3mm\nG92 E0					; Reset extruder position\nT0					; Select left extruder\nM140 S0					; Turn off bed heater\n\n; =================================	; Turn the rest off\nM107    				; Turn off fan\nM84					; Disable steppers\nM117 Print Complete",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 100,
    "print_speed": 80,
    "travel_speed": 120,
    "dia_feed": 2.85,
    "build_volume_x": 240,
    "build_volume_y": 225,
    "build_volume_z": 245,
}
