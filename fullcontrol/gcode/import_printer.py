
import json
import os
from copy import deepcopy
from fullcontrol.gcode import Extruder, ManualGcode, Buildplate, Hotend, Fan
import fullcontrol.devices.community.singletool.base_settings as base_settings
from importlib import import_module, resources


def load_json(library, file_name):
    resource = resources.files('fullcontrol') / 'devices' / library / file_name
    with resource.open('r') as file:
        return json.load(file)

def find_terms_in_brackets(input_string):
    import re
    ' find all terms in the start_gcode string contained within {} and split the terms if they are comma separated'
    matches = re.findall(r'\{(.*?)\}', input_string)
    split_matches = [item.split(',') for item in matches]
    cleaned_matches = [[item.strip() for item in sublist]
                       for sublist in split_matches]
    cleaned_matches = [item for sublist in cleaned_matches for item in sublist]
    return set(cleaned_matches)


def replace_gcode_variables(printer_name: str, gcode_type: str, data: dict):
    # 'data' is used during the eval process to replace variables in the gcode string
    variables = find_terms_in_brackets(data[gcode_type])
    if len(variables) > 0:
        new_start_end_gcode = data[gcode_type]
        for variable in variables:
            new_start_end_gcode = new_start_end_gcode.replace('{' + variable + '}', str(eval(variable)))
        data[gcode_type] = new_start_end_gcode


def import_printer(printer_name: str, user_overrides: dict):
    library_name = 'cura' if printer_name[:5] == 'Cura/' else 'community_minimal'
    printer_name = printer_name[5:] if library_name == 'cura' else printer_name[10:]
    library = load_json(library_name, os.path.join('library.json'))
    data = import_module(f'fullcontrol.devices.{library_name}.settings.{library[printer_name]}').default_initial_settings
    if library_name == 'cura':
        data['print_speed'] = int(data['print_speed']*60)
        data['travel_speed'] = int(data['travel_speed']*60)
    data = {**base_settings.default_initial_settings, **data}
    data = {**data, **user_overrides}
    original_start_gcode = deepcopy(data['start_gcode'])
    replace_gcode_variables(printer_name, 'start_gcode', data)
    replace_gcode_variables(printer_name, 'end_gcode', data)
    
    starting_procedure_steps = []
    starting_procedure_steps.append(ManualGcode(text=data['start_gcode']))
    starting_procedure_steps.append(ManualGcode(
        text=f'; Time to print!!!!!\n; Printer name: {printer_name}\n; GCode created with FullControl - tell us what you\'re printing!\n; info@fullcontrol.xyz or tag FullControlXYZ on Twitter/Instagram/LinkedIn/Reddit/TikTok \n; New terms added to the hard-coded start_gcode ensure user-overrides are implemented:'))
    starting_procedure_steps.append(Extruder(relative_gcode=data["relative_e"]))
    if 'bed_temp' in user_overrides.keys() and 'bed_temp' not in original_start_gcode:
        starting_procedure_steps.append(Buildplate(temp=data["bed_temp"], wait=True))
    if 'nozzle_temp' in user_overrides.keys() and 'nozzle_temp' not in original_start_gcode:
        starting_procedure_steps.append(Hotend(temp=data["nozzle_temp"], wait=True))
    if 'fan_percent' in user_overrides.keys() and 'fan_percent' not in original_start_gcode:
        starting_procedure_steps.append(Fan(speed_percent=data["fan_percent"]))
    if 'print_speed_percent' in user_overrides.keys() and 'print_speed_percent' not in original_start_gcode:
        starting_procedure_steps.append(ManualGcode(text='M220 S' + str(data["print_speed_percent"])+' ; set speed factor override percentage'))
    if 'material_flow_percent' in user_overrides.keys() and 'material_flow_percent' not in original_start_gcode:
        starting_procedure_steps.append(ManualGcode(text='M221 S' + str(data["material_flow_percent"])+' ; set extrude factor override percentage'))
    data['starting_procedure_steps'] = starting_procedure_steps
    data['ending_procedure_steps'] = [ManualGcode(text=data['end_gcode'])]

    return data
