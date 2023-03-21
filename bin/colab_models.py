
# colab_models.py - save new copies of model notebooks that work with google colab (new notebooks saved in models/colab directory)

usage = '  usage: python colab_models.py'  # executed from the bin folder of repo

notebook_names = ["nonplanar_spacer.ipynb",
                  "nuts_and_bolts.ipynb"]

notebook_addresses = ["../models/" + notebook_name for notebook_name in notebook_names]

old_import = "import fullcontrol as fc"
new_import = "if 'google.colab' in str(get_ipython()):\\n  !pip install git+https://github.com/FullControlXYZ/fullcontrol --quiet\\n" + old_import

for notebook_address in notebook_addresses:
    content_string = open(notebook_address).read()
    # replace import statement with install+import statements:
    content_string = content_string.replace(old_import, new_import)
    open(f'{notebook_address[:-6].replace("models","models/colab")}_colab.ipynb', 'w').write(content_string)
