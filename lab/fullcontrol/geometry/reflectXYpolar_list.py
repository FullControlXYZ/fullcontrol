from fullcontrol.geometry import Point, reflectXYpolar


def reflectXYpolar_list(steps: list, p_reflect: Point, angle_reflect: float) -> list:
    '''creates a reverse-ordered copy of the supplied steplist and applies the reflectXYpolar function 
    to all Points in the list. Elements that are not Points cause an error for now because the position 
    of commands in the list may need to change (e.g. turning extrusion on or off)
    '''
    new_steplist = []
    for i in range(len(steps)):
        step_now = (len(steps)-1)-i
        if type(steps[step_now]).__name__ != "Point":
            raise Exception(
                f'list of steps contained a {type(steps[step_now]).__name__}. only Points can be included in the list being reflected for now. Other types of objects needs careful consideration in terms of sequencing.')
        new_steplist.append(reflectXYpolar(steps[step_now], p_reflect, angle_reflect))
    return new_steplist
