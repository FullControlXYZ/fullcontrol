from fullcontrol.gcode import ManualGcode


def set_up(user_overrides: dict):
    ''' DO THIS
    '''

    # copy the ender_3 initialization data except change one line in the starting procedure
    import fullcontrol.devices.community.singletool.toolchanger_T0
    initialization_data = fullcontrol.devices.community.singletool.toolchanger_T0.set_up(user_overrides)
    initialization_data['starting_procedure_steps'][2] = ManualGcode(text='T3')

    return initialization_data
