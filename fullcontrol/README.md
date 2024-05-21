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
    1. interesting subpackage **fullcontrol/gcode/primer_library**: 
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
1. **fullcontrol/devices**
    1. this subpackage contains libraries of systems (3D printers) which is used to format gcode correctly for a given system
    1. three printer libraries exist currently: ***community***, ***community_minimal***, and ***cura***
        1. ***community*** (**fullcontrol/devices/community**) is a community-created library of 3D printers in a format that most embraces the fullcontrol design method
            1. starting procedures are defined instead of start_gcode strings as have been used historically. this means the procedures can easily adapt to other manufacturing platforms (e.g. robots)
            1. base_settings.py defines default printer settings
            1. other modules in this subpackage import base_settings.py to initialize a printer
            1. currently set up for single tool system, but could extend to multitool if desired
        1. ***community_minimal*** (**fullcontrol/devices/community_minimal**) implements a much simpler printer definition
            1. start_gcode and end_gcode are written as strings
            1. these strings can contain references to other settings (e.g. nozzle temperature) within the printer library entry or base_settings.py or initialization_data in GcodeControls supplied by the user
            1. these strings can also contain code within {} that is evaluated during gcode generation
            1. aside from these strings, the other only information that must be defined is the printer name. all other settings are inherited from base_setting.py, so are optional.
        1. ***cura*** (**fullcontrol/devices/cura**) adopts the format of ***community_minimal*** with start/end gcode strings stored alongside other relevant printer information, but the data has been extracted from the cura printer library
    1. to add a new printer:
        1. in ***community***:
            1. copy an existing module (e.g. ultimaker2plus.py)
            1. rename it to your printer name
            1. change 'printer_overrides', 'starting_procedure_steps' and 'ending_procedure_steps' - leave the rest of the module unchanged
            1. in your ***design*** set 'printer_name' in a GcodeControls object to be the name of the new module
        1. in ***community_minimal***:
            1. copy and existing module (e.g. generic.py or template.py) into fullcontrol/devices/community_minimal/settings
            1. update the printer name, start/end gcode entries and any other settings you wish
            1. update fullcontrol/devices/community_minimal/library.json to include your new printer name, which is written by the user in the design, and module filename
        1. in ***cura***:
            1. scripts have been created to extract the relevant information from all cura profiles, these can be re-run when the cura github repo updates. more information can be supplied if needed (raise as issue)
       


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
