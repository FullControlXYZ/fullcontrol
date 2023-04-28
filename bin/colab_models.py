
# colab_models.py - save new copies of model notebooks that work with google colab (new notebooks saved in models/colab directory)

usage = '  usage: python colab_models.py'  # executed from the bin folder of repo

notebook_names = ["nonplanar_spacer.ipynb",
                  "hex_adapter.ipynb",
                  "fractional_design_engine_polar.ipynb",
                  "ripple_texture.ipynb",
                  "nuts_and_bolts.ipynb"]

notebook_addresses = ["../models/" + notebook_name for notebook_name in notebook_names]

old_import = "import fullcontrol as fc"
new_import = "if 'google.colab' in str(get_ipython()):\\n  !pip install git+https://github.com/FullControlXYZ/fullcontrol --quiet\\n" + \
    old_import + "\\nfrom google.colab import files"
old_gcode = "gcode = fc.transform(steps, 'gcode', gcode_controls)"
new_gcode = old_gcode + "\\nopen(f'{design_name}.gcode', 'w').write(gcode)\\nfiles.download(f'{design_name}.gcode')"
old_gcode2 = "    save_as=design_name,"
new_gcode2 = ""


for notebook_address in notebook_addresses:
    content_string = open(notebook_address).read()
    # replace import statement with install+import statements:
    content_string = content_string.replace(old_import, new_import)
    content_string = content_string.replace(old_gcode, new_gcode)
    content_string = content_string.replace(old_gcode2, new_gcode2)
    open(f'{notebook_address[:-6].replace("models","models/colab")}_colab.ipynb', 'w').write(content_string)
