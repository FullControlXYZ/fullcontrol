from fullcontrol.common import Point
from itertools import chain
from copy import deepcopy


def points_only(steps: list, track_xyz: bool = True) -> list:
    ''' convert steps of Points and control to only Points. return new list. 
    If track_xyz=False, Points are returned as they are defined, including attributes with value=None
    If track_xyz=True, the returned list contains a tracked list of points with all of xyz
    defined: when some of xyz are not defined, they are calculated from previous step. The first point 
    in the returned list will be the first point for which all xyz were defined/tracked. 
    '''
    new_steps = []
    for step in steps:
        if isinstance(step, Point): # only consider Point data
            if (not track_xyz) or (not new_steps and all(val is not None for val in (step.x, step.y, step.z))):
                new_steps.append(step)
            else: # track_xyz, with at least one valid point already added
                # fill in any None attributes for the next point with the most recent previous value:
                next_point = deepcopy(new_steps[-1])
                # update values that are not None
                next_point.update_from(step)
                new_steps.append(next_point)


def flatten(steps: list) -> list:
    'takes a list in which some elements are lists in (second dimension). returns a flattenned 1D list'
    return list(chain.from_iterable(step if isinstance(step, list) else [step]
                                    for step in steps))


def linspace(start: float, end: float, number_of_points: int) -> list:
    'generate evenly spaced floats from start to end. returns a list of number_of_points floats including start and end'
    return [start + float(x)/(number_of_points-1)*(end-start) for x in range(number_of_points)]


def check(steps: list):
    'check a list of steps and report what type of classes are included and whether the list is 2D. FullControl requires it to be 1D for processing'
    # potential things to add to this function: check the first point has all of X Y Z defined
    if isinstance(steps, list):
        results = ""
        types = set(type(step).__name__ for step in steps)
        if "list" in types:
            results = "\n".join((
                "  warning - the list of steps must be a 1D list of fullcontrol class instances, it currently includes a 'list'",
                "  use fc.flatten() to convert it to 1D or check for accidental use of append() instead of extend()\n"
            ))
        results += f"  step types {types}"
    else:
        results = "  warning - the design must be a 1D list of fullcontrol class instances, it currently a single object, not a list"
    print("check results:\n" + results)


def first_point(steps: list, fully_defined: bool = True) -> Point:
    'return first Point in list. if the parameter fully_defined is true, return first Point with all x,y,z != None'
    if isinstance(steps, list):
        for step in steps:
            if isinstance(step, Point):
                if fully_defined and any(val is None for val in (step.x, step.y, step.z)):
                    continue
                return step
    if fully_defined:
        raise Exception('No point found in steps with all of x y z defined')
    if not fully_defined:
        raise Exception('No point found in steps')


def export_design(steps: list, filename: str):
    'export design (list of steps) to filename.json'
    import json
    with open(filename + '.json', 'w', encoding='utf-8') as f:
        json.dump(steps, f, ensure_ascii=False, indent=4, default=lambda x: {'type': type(x).__name__, 'data': x.__dict__})


def import_design(fc_module_handle, filename: str):
    'import a previously exported design (list of steps). fc_module_handle is the fc module that was imported to create the design originally (typically fc in documentation)'
    import json
    with open(filename + '.json') as f:
        data = json.load(f)
    steps = []
    for step in data:
        class_ = getattr(fc_module_handle, step['type'])
        step = class_.parse_obj(step['data'])
        steps.append(step)
    return steps
