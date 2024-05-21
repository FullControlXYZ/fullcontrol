from fullcontrol.gcode import ManualGcode


def set_up(user_overrides: dict):
    ''' DO THIS
    '''

    # copy the ender_3 initialization data except change one line in the starting procedure
    import fullcontrol.devices.community.singletool.ender_3
    initialization_data = fullcontrol.devices.community.singletool.ender_3.set_up(user_overrides)
    initialization_data['starting_procedure_steps'][1] = ManualGcode(text=';MAXX:300\n;MAXY:300\n;MAXZ:400\n')

    return initialization_data
