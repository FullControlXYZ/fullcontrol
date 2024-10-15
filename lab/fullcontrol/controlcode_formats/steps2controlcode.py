import os
import shutil
import zipfile
from importlib import resources
from lab.fullcontrol.controlcode_formats.controls import CodeControls
from fullcontrol import GcodeControls


def gcode_to_bambu_3mf(gcode: str, new_3mf_file: str):
    '''Convert gcode to bambu 3mf'''
    try: import google.colab; colab = True
    except ImportError: colab = False


    # Paths
    new_3mf_file = new_3mf_file[:-5] if new_3mf_file.endswith('.3mf') else new_3mf_file
    local_3mf = "/content/FC_bambulab_template.3mf" if colab else "FC_bambulab_template.3mf"
    extract_dir = "/content/extracted_3mf" if colab else "extracted_3mf"
    new_3mf_file = f"/content/{new_3mf_file}.3mf" if colab else f"{new_3mf_file}.3mf"


    # Step 0: Get the .3mf file from the installed Python package using importlib.resources
    with resources.files('lab.fullcontrol.controlcode_formats') / 'FC_bambulab_template.3mf' as package_3mf_path:
        # Copy the .3mf file to the local content directory
        if not os.path.exists(local_3mf):
            shutil.copy(package_3mf_path, local_3mf)

    # Step 1: Delete existing extracted folder and new .3mf if they exist
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    if os.path.exists(new_3mf_file):
        os.remove(new_3mf_file)

    # Step 2: Extract .3mf
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(local_3mf, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    plate_gcode_file = os.path.join(extract_dir, "Metadata", "plate_1.gcode")
    with open(plate_gcode_file, 'r+') as file:
        file.write(file.read().replace("; [FULLCONTROL GCODE HERE]", gcode))

    # Step 4: Repackage contents of FC_bambulab_template into a new .3mf
    fc_template_dir = os.path.join(extract_dir)
    with zipfile.ZipFile(new_3mf_file, 'w', zipfile.ZIP_DEFLATED) as new_zip:
        for foldername, subfolders, filenames in os.walk(fc_template_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                # Flatten the structure by ignoring FC_bambulab_template
                arcname = os.path.relpath(file_path, fc_template_dir)
                new_zip.write(file_path, arcname)

    # Step 5: Download the new .3mf
    if colab: 
        from google.colab import files
        files.download(new_3mf_file)

    # Step 6: Cleanup
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    if os.path.exists(local_3mf):
        os.remove(local_3mf)

def controlcode(steps: list, model_controls: CodeControls, show_tips: bool):

    if model_controls.code_format != '3mf':
        raise ValueError("only '3mf' is currently supported for CodeControls.code_format")
    
    if model_controls.code_format == '3mf':
        if not isinstance(model_controls.controls, GcodeControls):
            raise ValueError("CodeControls.controls must be a fc.GcodeControls instance at present")
        if model_controls.controls.printer_name != 'bambulab_x1':
            raise ValueError("only 'bambulab_x1' is currently supported for CodeControls.controls.printer_name")
        if model_controls.controls.save_as != None:
            raise ValueError("for fc.transform to 'control_code', and specifically 3mf, don't use GcodeControl.save_as, use CodeControls.filename instead")
        from fullcontrol.gcode.steps2gcode import gcode
        from fullcontrol.common import fix
        steps = fix(steps, 'gcode', model_controls.controls)
        gcode_str = gcode(steps, model_controls.controls, show_tips)

        gcode_str = gcode_str.split('\n')
        gcode_str = gcode_str[:15] + gcode_str[16:20] + gcode_str[22:]
        print('during 3mf generation, gcode lines for aux fan, purge and rise were deleted from the bamulab starting procedure')
        gcode_str = '\n'.join(gcode_str)

        gcode_to_bambu_3mf(gcode_str, model_controls.filename)

