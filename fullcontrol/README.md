# FullControl python package

more details of the structure of this library will be given in a future release of FullControl aimed at developers

however, it is briefly summarised here along with instructions for some modifications anticipated to be quite common (e.g. adding a new printer / changing the format of gcode strings)

## structure

the structure of the fullcontrol package and subpackages are likely to change considerably. any efforts to add new functionality should be done with an understanding that such changes will likely need to be significantly edited to work with future releases of FullControl

1. **fullcontrol**
    1. top-level modules define generic classes for FullControl's ***state***-changing objects
    1. attributes/methods at the top level are relevant to common ***state*** in extrusion additive manufacturing
    1. **common.py** imports relevant classes/functions from these modules for easy import into subpackages
    1. **\_\_init\_\_.py** imports the classes/functions with capabilities for both gcode and visualization (**fullcontrol/combinations** described below) to achieve a simple import statement by the end user
1. **fullcontrol/gcode**
    1. most modules in the gcode subpackage import the generic classes defined in the top-level modules and add new gcode-specific attributes and methods
    1. other modules create new functions and objects to control the generation of gcode
    1. **\_\_init\_\_.py** imports relevant classes/functions from these modules
    1. the module **fullcontrol/gcode/point.py** can be edited to change the text string format of gcode 
    1. interesting subpackages:
        1. **fullcontrol/gcode/printer_library/singletool**: 
            - base_settings.py defines default printer settings
            - other modules in this subpackage import base_settings.py and initialize a printer. to add a new printer:
                1. copy an existing module (e.g. ultimaker2plus.py)
                1. rename it to your printer name
                1. change 'printer_overrides', 'starting_procedure_steps' and 'ending_procedure_steps' - leave the rest of the module unchanged
                1. in your ***design*** set 'printer_name' in a GcodeControls object to be the name of the new module
        1. **fullcontrol/gcode/primer_library**: 
            - modules here are the primer options included in FullControl - they add steps to the beginning of a ***design***
            - if you want to add a new primer to FullControl rather than include primer steps directly in a ***design***, do the following: 
                1. copy, paste, rename, and edit an existing primer module (e.g. x.py) to create a custom primer routine
                1. use a GcodeControls object with {"primer": "name_of_new_module_excluding_.py"} included in the initialization_data parameter when transforming the ***design*** to a gcode ***result***
1. **fullcontrol/visualize**
    1. most modules in the visualize subpackage import the generic classes defined in the top-level modules and add new attributes and methods to generate a visual preview
    1. other modules create new functions and objects to control the generation of the visual preview
    1. **\_\_init\_\_.py** imports relevant classes/functions from these modules
1. **fullcontrol/combinations**
    1. this subpackage is used to combine functionality in multiple ***result***-specific subpackages
    1. the conceptual approach and code in this subpackage are likely to change significantly in the future
    1. the module **fullcontrol/combinations/gcode_and_visualize/common.py** imports relevant classes/functions for the current implementation of FullControl (gcode and visualize)
1. **fullcontrol/geometry**
    1. modules in this subpackage define functions that create/modify/measure geometry, where 'geometry' refers to a point or list of points. 
    1. **\_\_init\_\_.py** imports relevant classes/functions from these modules
    1. the import order in **\_\_init\_\_.py** is important since the modules import functions from each other
    1. in the currently implementation, points created in this subpackage have both gcode and visualize functionality. hence the import of Point from **fullcontrol.combinations.gcode_and_visualize.classes** at the top of **\_\_init\_\_.py** - this means all the modules in this subpackage generate Points with relevant attributes/methods for both gcode and visualize ***results***. similar for the Extruder object 
    1. adding new geometry functions to existing modules, or adding new modules by copying and editing one of the existing modules, is possible if the appropriate import statement is edited or added to the bottom of **\_\_init\_\_.py**. However, such additions may require a greater understanding of the FullControl code than intended for this initial release of FullControl (e.g. to avoid circular imports). currently, it is advised to create new geometry functions in your ***design*** script rather than editing the FullControl package


## lab package structure

in addition to the 'fullcontrol' package, there is a 'lab.fullcontrol' package

1. **lab/fullcontrol**
    1. **\_\_init\_\_.py** imports relevant classes/functions from **lab/fullcontrol/geomtry** to achieve a simple import statement by the end user
    1. **fiveaxis.py** imports the relevant classes/functions from **lab/fullcontrol/multiaxis** to achieve a simple import statement by the end user
    1. subpackages:
        1. **lab/fullcontrol/geomtry**
            1. extra geometric features to supplement those in the regular FullControl package
        1. **lab/fullcontrol/multiaxis**
            1. demo implementation of five-axis toolpath design. this demo was not created to be adaptable to different hardware systems. more flexibility to alternative printing hardware will be considered for future releases of FullControl along with additional functionality
