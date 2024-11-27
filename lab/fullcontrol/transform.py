from lab.fullcontrol.geometry_model.controls import ModelControls
from fullcontrol import GcodeControls
from lab.fullcontrol.controlcode_formats.controls import CodeControls
from fullcontrol import transform as transform_original
from typing import Union
from lab.fullcontrol.laser.laser import Laser


def transform(steps: list, result_type: str, controls: Union[ModelControls, GcodeControls, CodeControls] = None, show_tips: bool = True):
    ''' Transform a fullcontrol design (a list of function class instances) into various output formats.
    Optionally, Controls can be passed to control how the output is generated.
    '''
    
    if result_type == 'control_code':  
        from lab.fullcontrol.controlcode_formats.steps2controlcode import controlcode 
        if controls is not None:
            controlcode(steps, controls, show_tips)
        else:
            controlcode(steps, CodeControls(), show_tips)
    elif result_type == '3d_model':
        from lab.fullcontrol.geometry_model.steps2geometry import geometry_model
        if controls is not None:
            geometry_model(steps, controls)
        else:
            print("warning: no controls were supplied to fclab.transform(). it's advisable to supply fclab.ModelControls. the simulated extrusion width and height may be incorrect")
            geometry_model(steps, ModelControls())
    elif result_type == 'laser_cutter_gcode':
        import re

        def remove_terms_from_gcode(gcode, term_characters):
            pattern = r'[' + ''.join(term_characters) + r']\d*\.?\d+ ?'
            return re.sub(pattern, '', gcode)
        
        if controls is None: controls = GcodeControls()

        # don't allow the gcode function to save gcode since we will modify it after generation
        if controls.save_as == True:
            raise Exception("please set GcodeControl.save_as = False for 'laser_cutter_gcode'")
        # force initialization data as first object in design
        if not isinstance(steps[0], Laser):
            raise Exception("first object in design must be an fclab.Laser() object")
        else:
            for attribute in ['cutting_speed', 'travel_speed', 'spotsize', 'on']:
                if getattr(steps[0], attribute) is None:
                    raise Exception(f"first object in design (fclab.Laser) must have all attributes set - attribute '{attribute}' is missing")
            if steps[0].constant_power == None and steps[0].dynamic_power == None:
                raise Exception("first object in design (fclab.Laser) must have either 'constant_power' or 'dynamic_power' set")
        gcode = transform_original(steps, 'gcode', controls, show_tips)
        gcode = remove_terms_from_gcode(gcode, ['Z', 'E'])
        # remove relative extrusion gcode command
        gcode = gcode.replace("M83 ; relative extrusion\n", "")
        return gcode
    else:
        raise ValueError(f"result_type '{result_type}' not recognized. Please use 'control_code', '3d_model', 'laser_cutter_gcode', or fc.transform()")




