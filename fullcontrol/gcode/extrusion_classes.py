from typing import Optional
from fullcontrol.common import ExtrusionGeometry as BaseExtrusionGeometry
from fullcontrol.common import Extruder as BaseExtruder
from fullcontrol.common import StationaryExtrusion as BaseStationaryExtrusion
from fullcontrol.gcode import Point
# from fullcontrol.geometry.measure import distance_forgiving
from math import pi
from pydantic import root_validator


class ExtrusionGeometry(BaseExtrusionGeometry):
    'Extend generic class with gcode method to convert the object to gcode'
    def gcode(self, state):
        '''
        Process this instance in a list of steps supplied by the designer to generate and return a line of gcode.

        Args:
            state (State): The state object containing the extrusion geometry.

        Returns:
            str: The generated line of gcode.
        '''
        # update all attributes of the tracking instance with the new instance (self)
        state.extrusion_geometry.update_from(self)
        if self.width != None \
                or self.height != None \
                or self.diameter != None \
                or self.area_model != None:
            try:
                state.extrusion_geometry.update_area()
            except:
                pass  # in case not all parameters set yet


class StationaryExtrusion(BaseStationaryExtrusion):
    'Extend generic class with gcode method to convert the object to gcode'
    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        state.printer.speed_changed = True
        return f'G1 F{self.speed} E{state.extruder.get_and_update_volume(self.volume)*state.extruder.volume_to_e:.6}'


class Extruder(BaseExtruder):
    '''
    Extend generic class with gcode methods and attributes to convert the object to gcode.

    This class is used to manage the state of the extruder and translate the design into GCode.

    Attributes:
        units (str, optional): The units for E in GCode. Options include 'mm' and 'mm3'. If not specified, a default unit is used.
        dia_feed (float, optional): The diameter of the feedstock filament.
        relative_gcode (bool, optional): A flag indicating whether to use relative GCode. If not specified, a default value is used.
        volume_to_e (float, optional): A factor to convert the volume of material into the value of 'E' in GCode. Calculated automatically.
        total_volume (float, optional): The current extrusion volume for the whole print. Calculated automatically.
        total_volume_ref (float, optional): The total extrusion volume reference value. This attribute is set to allow extrusion to be expressed relative to this point. For relative_gcode = True, it is reset for every line. Calculated automatically.
        travel_format (str, optional): The format for travel moves in the GCode. If not specified, a default format is used.
    '''

    # gcode additions to generic Extruder class

    # GCode attributes, used to translate the design into gcode:
    # units for E in GCode ... options: 'mm' / 'mm3'
    units: Optional[str] = None
    dia_feed: Optional[float] = None  # diameter of the feedstock filament
    relative_gcode: Optional[bool] = None
    # attibutes not set by user ... calculated automatically:
    # factor to convert volume of material into the value of 'E' in gcode
    volume_to_e: Optional[float] = None
    # current extrusion volume for whole print
    total_volume: Optional[float] = None
    # total extrusion volume reference value - this attribute is set to allow extrusion to be expressed relative to this point (for relative_gcode = True, it is reset for every line)
    total_volume_ref: Optional[float] = None
    travel_format: Optional[str] = None

    def get_and_update_volume(self, volume):
        '''Calculate the extrusion volume and update the total volume.

        Args:
            volume (float): The volume of material to be extruded.

        Returns:
            float: The extrusion volume relative to the total volume.
        '''
        self.total_volume += volume
        ret_val = self.total_volume - self.total_volume_ref
        if self.relative_gcode == True:
            self.total_volume_ref = self.total_volume
        # to make absolute extrusion work, check self.total_volume_ref and, if above a treshold value, reset extrusion (set extruder_now.e_total_vol_reference_for_gcode = extruder_now.e_total_vol; insert a G92 command next in the steplist)
        return ret_val

    def e_gcode(self, point1: Point, state) -> str:
        '''Generate the gcode for extrusion.

        Args:
            point1 (Point): The point at the end of the extrusion.
            state: The current state of the printer.

        Returns:
            str: The gcode component for extrusion.
        '''
        def distance_forgiving(point1: Point, point2: Point) -> float:
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
        if self.on:
            # length = pt1.distance_to_self(pt2)
            length = distance_forgiving(point1, state.point)
            return f'E{self.get_and_update_volume(length*state.extrusion_geometry.area)*self.volume_to_e:.6f}'.rstrip('0').rstrip('.')
        else:
            if state.extruder.travel_format == 'G1_E0':
                # return 'E0' for relative extrusion or E(previous extrusion) for absolute extrusion
                return f'E{self.get_and_update_volume(0)*self.volume_to_e:.6f}'.rstrip('0').rstrip('.')
            else: 
                # return nothing if travel format does not require am E value
                return ''

    def update_e_ratio(self):
        '''Calculate the ratio for conversion from mm3 extrusion to units for E in gcode.'''
        try:  # try in case not all parameters set yet
            if self.units == "mm3":
                self.volume_to_e = 1
            elif self.units == "mm":
                self.volume_to_e = 1 / (pi*(self.dia_feed/2)**2)
        except:
            pass

    def gcode(self, state):
        '''Process this instance in a list of steps supplied by the designer to generate and return a line of gcode.

        Args:
            state: The current state of the printer.

        Returns:
            str: The generated line of gcode.
        '''
        # update all attributes of the tracking instance with the new instance (self)
        state.extruder.update_from(self)
        # do things for each attribute that was changed by the designer. check for changes in the new Extruder (self) but calculations consider the overall current Extruder (extruder_now)
        if self.on != None:
            # change in case strategy changed from printing to moving fast without extrusion
            state.printer.speed_changed = True
        if self.units != None or self.dia_feed != None:
            state.extruder.update_e_ratio()
        if self.relative_gcode != None:
            state.extruder.total_volume_ref = state.extruder.total_volume
            return "M83 ; relative extrusion" if state.extruder.relative_gcode == True else "M82 ; absolute extrusion\nG92 E0 ; reset extrusion position to zero"
