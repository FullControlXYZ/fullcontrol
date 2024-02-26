from lab.fullcontrol.geometry_model.controls import ModelControls

def transform(steps: list, result_type: str, controls: ModelControls = None):
    ''' Transform a fullcontrol design (a list of function class instances) into result_type "3d_model".
    Optionally, ModelControls can be passed to control how the 3D model is generated.
    '''
    if result_type == '3d_model':  # This is currently redundant, but maintained for consistency with fullcontrol.combinations.gcode_and_visualization.common in any future expansion to the result_type options here
        from lab.fullcontrol.geometry_model.steps2geometry import geometry_model
        if controls is not None:
            return geometry_model(steps, controls)
        return geometry_model(steps)
