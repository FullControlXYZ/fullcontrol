from typing import Optional
from fullcontrol.common import Point as BasePoint
from copy import deepcopy
import numpy as np

class Point(BasePoint):
    'generic gcode Point with 5-axis aspects added/modified'
    b: Optional[float] = None
    c: Optional[float] = None

    def XYZBC_gcode(self, self_systemXYZ, p) -> float:
        'generate XYZBC gcode string to move from a point p to this point. return XYZBC string'
        s = ''
        if self_systemXYZ.x != None and self_systemXYZ.x != p.x:
            s += f'X{round(self_systemXYZ.x, 6):.6} '
        if self_systemXYZ.y != None and self_systemXYZ.y != p.y:
            s += f'Y{round(self_systemXYZ.y, 6):.6} '
        if self_systemXYZ.z != None and self_systemXYZ.z != p.z:
            s += f'Z{round(self_systemXYZ.z, 6):.6} '
        if self_systemXYZ.b != None and self_systemXYZ.b != p.b:
            s += f'B{round(self_systemXYZ.b, 6):.6} '
        if self_systemXYZ.c != None and self_systemXYZ.c != p.c:
            s += f'C{round(self_systemXYZ.c, 6):.6} '
        return s if s != '' else None

    def inverse_kinematics(self, state):
        'calcualte system XYZ for the current point XYZ (in part coordinates)'

        def model2system(model_point, state, system_type: str):
            from math import cos, sin, tau
            system_point = deepcopy(model_point)
            if system_type == 'bc_bed':
                # # calculate XYZ as if B=0 first:
                # x_for_b0 = model_point.x*cos(model_point.c*tau/360) + model_point.y*-sin(model_point.c*tau/360)
                # y_for_b0 = model_point.y*cos(model_point.c*tau/360) + model_point.x*sin(model_point.c*tau/360)
                # z_for_b0 = model_point.z
                # # now calculate XYZ with effects of B rotation:
                # x_with_b = x_for_b0*cos(model_point.b*tau/360) + z_for_b0*sin(model_point.b*tau/360)
                # y_with_b = y_for_b0
                # z_with_b = z_for_b0*cos(model_point.b*tau/360) + x_for_b0*-sin(model_point.b*tau/360)
                # # now offset XYZ so the origin is positioned at the bc_intercept point in system coordinates
                # x_system = x_with_b + state.printer.bc_intercept.x
                # y_system = y_with_b + state.printer.bc_intercept.y
                # z_system = z_with_b + state.printer.bc_intercept.z
            # Update according to case point 5.3.2. Inverse Transformation https://linuxcnc.org/docs/html/motion/5-axis-kinematics.html
                inv_kin=np.zeros((3,3))
                inv_kin[0,:]= [cos(model_point.b*tau/360)*cos(model_point.c*tau/360), -sin(model_point.c*tau/360)*cos(model_point.b*tau/360), sin(model_point.b*tau/360)]
                inv_kin[1,:]= [sin(model_point.c*tau/360), cos(model_point.c*tau/360),0]
                inv_kin[2,:]= [-sin(model_point.b*tau/360)*cos(model_point.c*tau/360), sin(model_point.b*tau/360)*sin(model_point.c*tau/360), cos(model_point.b*tau/360)]

                inv_kin = np.matmul(inv_kin, np.array([model_point.x, model_point.y, model_point.z]))
                x_system = inv_kin[0]+state.printer.bc_intercept.x - sin(model_point.b*tau/360)*state.printer.bc_intercept.z - cos(model_point.b*tau/360)*state.printer.bc_intercept.x 
                y_system = inv_kin[1] # +state.printer.bc_intercept.y
                z_system = inv_kin[2]+state.printer.bc_intercept.z * (-cos(model_point.b*tau/360)+1) + sin(model_point.b*tau/360)*state.printer.bc_intercept.x 
                
            system_point.x = round(x_system, 6)
            system_point.y = round(y_system, 6)
            system_point.z = round(z_system, 6)
            return system_point

        # make sure undefined attributes of the current point (self) are taken from the point in state
        model_point = deepcopy(state.point)
        model_point.update_from(self)
        # inverse kinematics:
        system_point = model2system(model_point, state, 'bc_bed')
        return system_point

    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        self_systemXYZ = self.inverse_kinematics(state)
        XYZBC_str = self.XYZBC_gcode(self_systemXYZ, state.point_systemXYZ)
        if XYZBC_str != None:  # only write a line of gcode if movement occurs
            G_str = 'G1 ' if state.extruder.on else 'G0 '
            F_str = state.printer.f_gcode(state)
            E_str = state.extruder.e_gcode(self, state)
            gcode_str = f'{G_str}{F_str}{XYZBC_str}{E_str}'
            state.printer.speed_changed = False
            state.point.update_from(self)
            state.point_systemXYZ.update_from(self_systemXYZ)
            return gcode_str.strip()  # strip the final space
