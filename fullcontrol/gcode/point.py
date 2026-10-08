from typing import Optional
from fullcontrol.common import Point as BasePoint


class Point(BasePoint):
    'Extend generic class with gcode methods to convert the object to gcode'

    def XYZ_gcode(self, p,always_print) -> float:
        '''
        Generate XYZ gcode string to move from a point p to this point.

        Args:
            p (Point): The point to move from.
            always_print (bool): If True alway include all coordinates. 

        Returns:
            str: The XYZ gcode string.

        '''
        s = ''
        if (self.x != None and self.x != p.x) or always_print == True:
            x = self.x if self.x != None else p.x
            s += f'X{x:.6f}'.rstrip('0').rstrip('.') + ' '
        if (self.y != None and self.y != p.y) or always_print == True:
            y = self.y if self.y != None else p.y
            s += f'Y{y:.6f}'.rstrip('0').rstrip('.') + ' '
        if (self.z != None and self.z != p.z) or always_print == True:
            z = self.z if self.z != None else p.z
            s += f'Z{z:.6f}'.rstrip('0').rstrip('.') + ' '
        return s if s != '' else None

    def gcode(self, state):
        '''
        Process this instance in a list of steps supplied by the designer to generate and return a line of gcode.

        Args:
            state (State): The state object containing printer and extruder information.

        Returns:
            str: The generated line of gcode.

        '''
        XYZ_str = self.XYZ_gcode(state.point,state.printer.always_print_xyz)
        if XYZ_str != None:  # only write a line of gcode if movement occurs
            G_str = 'G1 ' if state.extruder.on or state.extruder.travel_format == "G1_E0" else 'G0 '
            F_str = state.printer.f_gcode(state)
            E_str = state.extruder.e_gcode(self, state)
            gcode_str = f'{G_str}{F_str}{XYZ_str}{E_str}'
            state.printer.speed_changed = False
            state.point.update_from(self)
            return gcode_str.strip()  # strip the final space
