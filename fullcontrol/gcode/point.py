from typing import Optional
from fullcontrol.common import Point as BasePoint


class Point(BasePoint):
    'generic Point with gcode methods added'
    # gcode additions to generic Point class

    def XYZ_gcode(self, p) -> float:
        'generate XYZ gcode string to move from a point p to this point. return XYZ string'
        s = ''
        if self.x != None and self.x != p.x:
            s += f'X{round(self.x, 10):.6} '
        if self.y != None and self.y != p.y:
            s += f'Y{round(self.y, 10):.6} '
        if self.z != None and self.z != p.z:
            s += f'Z{round(self.z, 10):.6} '
        return s if s != '' else None

    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        XYZ_str = self.XYZ_gcode(state.point)
        if XYZ_str != None:  # only write a line of gcode if movement occurs
            G_str = 'G1 ' if state.extruder.on or state.extruder.travel_format == "G1_E0" else 'G0 '
            F_str = state.printer.f_gcode(state)
            E_str = state.extruder.e_gcode(self, state)
            gcode_str = f'{G_str}{F_str}{XYZ_str}{E_str}'
            state.printer.speed_changed = False
            state.point.update_from(self)
            return gcode_str.strip()  # strip the final space
