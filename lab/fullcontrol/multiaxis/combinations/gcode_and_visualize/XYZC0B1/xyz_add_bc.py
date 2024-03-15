from typing import Union
from .classes import Point


def xyz_add_bc(xyz_geometry: Union[Point, list]) -> Union[Point, list]:
    'covert geometry with xyz attributes and methods to include bc attributes (=None) and bc methods'
    if type(xyz_geometry).__name__ == "Point":
        pt = Point()
        pt.update_from(xyz_geometry)
        return pt
    else:
        geometry_new = []
        for i in range(len(xyz_geometry)):
            if type(xyz_geometry[i]).__name__ == 'Point':
                pt = Point()
                pt.update_from(xyz_geometry[i])
                geometry_new.append(pt)
            else:
                geometry_new.append(xyz_geometry[i])
        return geometry_new
