
# colab_models.py - save new copies of model notebooks that work with google colab (new notebooks saved in models/colab directory)

# executed from the bin folder of repo
usage = '  usage: python colab_models.py'

notebook_names = ["design_template.ipynb",
                  "nonplanar_spacer.ipynb",
                  "hex_adapter.ipynb",
                  "fractional_design_engine_polar.ipynb",
                  "ripple_texture.ipynb",
                  "nuts_and_bolts.ipynb",
                  "blob_printing.ipynb",
                  "anyangle_phone_stand.ipynb",
                  "star_polygon_lattice.ipynb"]

notebook_addresses = ["../models/" + notebook_name for notebook_name in notebook_names]

old_intro = "*this document is a jupyter notebook - if they're new to you, check out how they work: [link](https://www.google.com/search?q=ipynb+tutorial), [link](https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb), [link](https://colab.research.google.com/)*"
new_intro = "*this document is a jupyter notebook - if they're new to you, check out how they work: [link](https://www.google.com/search?q=ipynb+tutorial), [link](https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb), [link](https://colab.research.google.com/)*\\n### be patient :)\\n\\nthe next code cell may take a while because running it causes several things to happen:\\n- connect to a google colab server -> download the fullcontrol code -> install the fullcontrol code\\n\\ncheck out [other tutorials](https://github.com/FullControlXYZ/fullcontrol/blob/master/tutorials/README.md) to understand the python code for the FullControl design"
old_intro_runall = 'run all cells in this notebook'
new_intro_runall = 'press ctrl+F9 to run all cells in this notebook'
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
    content_string = content_string.replace(old_intro_runall, new_intro_runall)
    content_string = content_string.replace(old_intro, new_intro)
    content_string = content_string.replace(old_import, new_import)
    # the next if statement accomodates notebooks that use "if target == 'gcode':"
    if "    gcode = fc.transform(steps, 'gcode', gcode_controls)" in content_string:
        content_string = content_string.replace(            old_gcode, new_gcode.replace("\\n", "\\n    "))
    else:
        content_string = content_string.replace(old_gcode, new_gcode)
    content_string = content_string.replace(old_gcode2, new_gcode2)
    open(f'{notebook_address[:-6].replace("models","models/colab")}_colab.ipynb',
         'w').write(content_string)
