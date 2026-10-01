from typing import Optional
from fullcontrol import Point as BasePoint
from copy import deepcopy
import numpy as np

from lab.fullcontrol.infinaxis.axis import Axis


def _model_field_names(model_class):
    return set(model_class.model_fields if hasattr(model_class, "model_fields") else model_class.__fields__)


def _axis_names(head_chain=None, bed_chain=None):
    axes = list(head_chain or []) + list(bed_chain or [])
    return {axis.name for axis in axes if axis.name is not None}


def configure_point(head_chain=None, bed_chain=None):
    """Return a Point class whose extra constructor fields map to configured axes."""
    axis_name_lookup = {name.lower(): name for name in _axis_names(head_chain, bed_chain)}

    class ConfiguredPoint(Point):
        # Keep axes as the storage model. This class is only a user-facing
        # convenience so designs can write Point(x=..., b=...) and point.b.
        def __init__(self, **data):
            fields = _model_field_names(type(self))
            field_lookup = {name.lower(): name for name in fields}
            axes = dict(data.pop("axes", None) or {})
            for name in list(data):
                if name not in fields and name.lower() in field_lookup:
                    data[field_lookup[name.lower()]] = data.pop(name)
                elif name.lower() in axis_name_lookup and name not in fields:
                    axes[axis_name_lookup[name.lower()]] = data.pop(name)
            if axes:
                data["axes"] = axes
            super().__init__(**data)

        def __getattr__(self, name):
            axes = getattr(self, "axes", None)
            axis_name = axis_name_lookup.get(name.lower())
            if axes is not None and axis_name in axes:
                return axes[axis_name]
            raise AttributeError(name)

        def __setattr__(self, name, value):
            axis_name = axis_name_lookup.get(name.lower())
            if axis_name is not None and name not in _model_field_names(type(self)):
                axes = dict(getattr(self, "axes", None) or {})
                axes[axis_name] = value
                super().__setattr__("axes", axes)
            else:
                super().__setattr__(name, value)

    return ConfiguredPoint


class Point(BasePoint):
    axes: Optional[dict] = None # dictionary for assigning chages to the printer Axis based on the info in the point

    def infinaxis_gcode(self, self_systemXYZ,state):
        'generate XYZABC gcode string to move from a point p to this point. return XYZABC string'
        p = state.point_systemXYZ
        always_print = state.Printer.always_print_geometry
        s = ''
        if (self_systemXYZ.x != None and self_systemXYZ.x != p.x) or always_print == True:
            x = self_systemXYZ.x if self_systemXYZ.x != None else p.x
            s += f'X{round(state.printer.xyz_orientation[0] * x, 6):.6} '
        if (self_systemXYZ.y != None and self_systemXYZ.y != p.y) or always_print == True:
            y = self_systemXYZ.y if self_systemXYZ.y != None else p.y
            s += f'Y{round(state.printer.xyz_orientation[1] * y, 6):.6} '
        if (self_systemXYZ.z != None and self_systemXYZ.z != p.z) or always_print == True:
            z = self_systemXYZ.z if self_systemXYZ.z != None else p.z
            s += f'Z{round(state.printer.xyz_orientation[2] * z, 6):.6} '
        
        # Currently this has no way of checking if movement occured in the chain axis, meaning they will always be included in the gcode output...
        for axis in state.printer.head_chain + state.printer.bed_chain:
            if axis.active != None:
                s += f'{axis.name}{round(float(axis.active), 12):.12} '

        return s if s != '' else None

    def inverse_kinematics(self, state):
        'calcualte system XYZ for the current point XYZ (in part coordinates)'
        def distance_forgiving(point1: Point, point2: Point) -> float: # copied from https://github.com/FullControlXYZ/fullcontrol/blob/master/fullcontrol/gcode/extrusion_classes.py
            '''Calculate the distance between two points. x, y or z components are ignored unless defined in both points

            Args:
                point1 (Point): The first point.
                point2 (Point): The second point.

            Returns:
                float: The distance between the two points.
            '''
            dist_x = 0 if point1.x == None or point2.x == None else point1.x - point2.x
            dist_y = 0 if point1.y == None or point2.y == None else point1.y - point2.y
            dist_z = 0 if point1.z == None or point2.z == None else point1.z - point2.z
            return ((dist_x)**2+(dist_y)**2+(dist_z)**2)**0.5

        def model2system(model_point, state):
            from math import cos, sin, tau
            system_point = deepcopy(model_point)

            def chain_matrix(chain,start_point=Point(x=0,y=0,z=0)):
                rev_chain = chain[::-1]
                M = np.matrix([[start_point.x],[start_point.y],[start_point.z]])
                for axis in rev_chain:
                    Mo = np.matrix([[axis.offset.x],[axis.offset.y],[axis.offset.z]]) if axis.offset != None else np.matrix([[0],[0],[0]])
                    M += Mo
                    if axis.type in ['X','Y','Z']:
                        i = 'XYZ'.index(axis.type)
                        M[i,0] += axis.active * axis.orientation
                    elif axis.type in ['A','B','C']:
                        angle_rad = axis.active * axis.orientation * tau / 360
                        if axis.type == 'A':
                            Mrot = np.matrix([[1,0,0],[0,cos(angle_rad),-sin(angle_rad)],[0,sin(angle_rad),cos(angle_rad)]])
                        elif axis.type == 'B':
                            Mrot = np.matrix([[cos(angle_rad),0,sin(angle_rad)],[0,1,0],[-sin(angle_rad),0,cos(angle_rad)]])
                        elif axis.type == 'C':
                            Mrot = np.matrix([[cos(angle_rad),-sin(angle_rad),0],[sin(angle_rad),cos(angle_rad),0],[0,0,1]])
                        M = np.matmul(Mrot, M)
                return M

            head = state.printer.head_chain
            bed = state.printer.bed_chain

            Mh = chain_matrix(head)
            Mb = chain_matrix(bed,model_point)

            Msystem = Mb-Mh
            x_system = Msystem.item(0) + state.printer.post_ik_offset.x
            y_system = Msystem.item(1) + state.printer.post_ik_offset.y
            z_system = Msystem.item(2) + state.printer.post_ik_offset.z

            system_point.x = round(x_system, 6)
            system_point.y = round(y_system, 6)
            system_point.z = round(z_system, 6)

            return system_point

        # make sure undefined attributes of the current point (self) are taken from the point in state
        model_point = deepcopy(state.point)
        model_point.update_from(self)
        # Update Axis from point
        if self.axes is not None:
            for axis in state.printer.head_chain + state.printer.bed_chain:
                if axis.name in self.axes and self.axes[axis.name] != None:
                    axis.active = self.axes[axis.name]

        # inverse kinematics:
        system_point = model2system(model_point, state)

        #calculate distance from
        dist = distance_forgiving(model_point,state.point)
        dist_system = distance_forgiving(system_point,state.point_systemXYZ)
        return system_point, dist, dist_system

    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        self_systemXYZ, dist, dist_system = self.inverse_kinematics(state)
        infinaxis_str = self.infinaxis_gcode(self_systemXYZ,state)
        if infinaxis_str != None:  # only write a line of gcode if movement occurs
            G_str = 'G1 ' if state.extruder.on else 'G0 '
            E_str = state.extruder.e_gcode(self, state)

            if state.printer.inverse_time_feedrate and state.extruder.on:
                if dist !=0:
                    f = 1 / (dist/state.printer.print_speed)
                else: # this case should only happen for pure orientation moves, so the print speed is used to allow the user to control it through normal fullcontrol means.
                    f=state.printer.print_speed

            elif state.printer.planning_axes_mono or state.printer.planning_axes_tripple: #For printers with planning axes, but no inverse time feedrate
                f = state.printer.print_speed
            else: # If the printer has no helper features.... with rounded f this is known to cause unintended printer behaviour
                if (dist != 0 and dist_system != 0): # (F-hacking) adjust feedrate based on the ratio of model distance to system distance to help keep print speed consistent.
                    f = state.printer.print_speed * (dist_system/dist)  
                else:
                    f = state.printer.print_speed 

            if state.printer.f_round:
                F_str = f'F{round(f, 0):.0f} '
            else:
                F_str = f'F{round(float(f), 6):.6} '
        
            if state.printer.planning_axes_mono or state.printer.planning_axes_tripple:
                state.distance_accumulated += dist

            if state.printer.planning_axes_tripple:
                axis_names = state.printer.planning_axes_names
                infinaxis_str = infinaxis_str + f"{axis_names[0]}{round(self.x, 6):.6} {axis_names[1]}{round(self.y, 6):.6} {axis_names[2]}{round(self.z, 6):.6} "
            elif state.printer.planning_axes_mono:
                axis_name = state.printer.planning_axes_names[0]
                infinaxis_str = infinaxis_str + f"{axis_name}{state.distance_accumulated:.3f} "
            gcode_str = f'{G_str}{F_str}{infinaxis_str}{E_str}'
            if state.printer.verbose:
                gcode_str += f' ; distance: {dist:.3f}, system: {dist_system:.3f}' 
            state.printer.speed_changed = False
            state.point.update_from(self)
            state.point_systemXYZ.update_from(self_systemXYZ)
            return gcode_str.strip()  # strip the final space
    
    def visualize(self, state: 'State', plot_data: 'PlotData', plot_controls: 'PlotControls'):
        '''
        Process a Point in a list of steps supplied by the designer to update plot_data and state.

        Args:
            state ('State'): The current state of the plot.
            plot_data ('PlotData'): The data used for plotting.
            plot_controls ('PlotControls'): The controls for plotting.

        Returns:
            None
        '''

        change_check = False
        precision_xyz = 3  # number of decimal places to use for x y z values in plot_data
        if self.x != None and self.x != state.point.x:
            state.point.x = round(self.x, precision_xyz)
            change_check = True
        if self.y != None and self.y != state.point.y:
            state.point.y = round(self.y, precision_xyz)
            change_check = True
        if self.z != None and self.z != state.point.z:
            state.point.z = round(self.z, precision_xyz)
            change_check = True
        if self.color != None and self.color != state.point.color:
            state.point.color = self.color
            change_check = True
        if change_check:
            state.point.update_color(state, plot_data, plot_controls)
            plot_data.paths[-1].add_point(state)
            state.point_count_now += 1
