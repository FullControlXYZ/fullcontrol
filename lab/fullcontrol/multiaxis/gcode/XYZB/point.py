from typing import Optional
from fullcontrol.common import Point as BasePoint
from copy import deepcopy


class Point(BasePoint):
    'generic gcode Point with 4-axis aspects added/modified'
    b: Optional[float] = None

    def XYZB_gcode(self, self_systemXYZ, p) -> float:
        'generate XYZBC gcode string to move from a point p to this point. return XYZB string'
        s = ''
        if self_systemXYZ.x != None and self_systemXYZ.x != p.x:
            s += f'X{round(self_systemXYZ.x, 6):.6} '
        if self_systemXYZ.y != None and self_systemXYZ.y != p.y:
            s += f'Y{round(self_systemXYZ.y, 6):.6} '
        if self_systemXYZ.z != None and self_systemXYZ.z != p.z:
            s += f'Z{round(self_systemXYZ.z, 6):.6} '
        if self_systemXYZ.b != None and self_systemXYZ.b != p.b:
            s += f'B{round(self_systemXYZ.b, 6):.6f} '
        return s if s != '' else None

    def inverse_kinematics(self, state):
        'calculate system XYZ for the current point XYZ (in part coordinates)'

        def model2system(model_point, state, system_type: str):
            from math import cos, sin, radians
            system_point = deepcopy(model_point)
            if system_type == 'b_nozzle':
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

                # OLD, WORKING STUFF:
                # # calculate X Z changes due to b roations:
                # x_system = model_point.x + state.printer.b_offset_z * sin(radians(model_point.b))
                # y_system = model_point.y
                # z_system = model_point.z - state.printer.b_offset_z * (1-cos(radians(model_point.b)))

                # if state.printer.b_offset_x:
                #     raise Exception(
                #         'b_offset_x parameter was set by the user but the inverse kinematicscode is not developed for that parameter yet')

                # calculate X Z changes due to b roations (these were identified intuitively):
                # x_system = model_point.x + \
                #     state.printer.b_offset_z * sin(radians(model_point.b)) - \
                #     state.printer.b_offset_x * (1-cos(radians(model_point.b)))
                # y_system = model_point.y
                # z_system = model_point.z - \
                #     state.printer.b_offset_z * (1-cos(radians(model_point.b))) - \
                #     state.printer.b_offset_x * sin(radians(model_point.b))
                b = radians(model_point.b)
                nozzle_offset_x, nozzle_offset_z = - \
                    state.printer.b_offset_x, -state.printer.b_offset_z
                nozzle_offset_from_b0_x = - \
                    (nozzle_offset_x*(1-cos(b))) + nozzle_offset_z*sin(b)
                nozzle_offset_from_b0_z = - \
                    (nozzle_offset_z*(1-cos(b))) + nozzle_offset_x*-sin(b)
                x_system = model_point.x - nozzle_offset_from_b0_x
                y_system = model_point.y
                z_system = model_point.z - nozzle_offset_from_b0_z

                # # the following lines are based on the standard equation to rotate a point about another point
                # # they assume the nozzle is vertical when b=0
                # # the next lines use -model_point.b because the y axis is oriented in the opposite direction from the z axis in XY rotations, which this equations were based on
                # nozzle_offset_x = -state.printer.b_offset_x
                # nozzle_offset_z = -state.printer.b_offset_z
                # nozzle_move_x = nozzle_offset_x * cos(radians(-model_point.b)) - \
                #     nozzle_offset_z * sin(radians(-model_point.b)) - \
                #     nozzle_offset_x
                # nozzle_move_z = nozzle_offset_x * sin(radians(-model_point.b)) + \
                #     nozzle_offset_z * cos(radians(-model_point.b)) - \
                #     nozzle_offset_z
                # x_system = model_point.x - nozzle_move_x
                # y_system = model_point.y
                # z_system = model_point.z - nozzle_move_z

            system_point.x = round(x_system, 6)
            system_point.y = round(y_system, 6)
            system_point.z = round(z_system, 6)
            system_point.b = round(model_point.b, 6)
            return system_point

        # make sure undefined attributes of the current point (self) are taken from the point in state
        model_point = deepcopy(state.point)
        model_point.update_from(self)
        # inverse kinematics:
        system_point = model2system(model_point, state, 'b_nozzle')
        return system_point

    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        self_systemXYZ = self.inverse_kinematics(state)
        XYZB_str = self.XYZB_gcode(self_systemXYZ, state.point_systemXYZ)
        if XYZB_str != None:  # only write a line of gcode if movement occurs
            G_str = 'G1 ' if state.extruder.on else 'G0 '
            F_str = state.printer.f_gcode(state)
            E_str = state.extruder.e_gcode(self, state)
            gcode_str = f'{G_str}{F_str}{XYZB_str}{E_str}'
            state.printer.speed_changed = False
            state.point.update_from(self)
            state.point_systemXYZ.update_from(self_systemXYZ)
            return gcode_str.strip()  # strip the final space
