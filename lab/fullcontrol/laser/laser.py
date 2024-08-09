from typing import Optional
from fullcontrol.common import BaseModelPlus
from fullcontrol import Printer, Extruder, ExtrusionGeometry, ManualGcode


class Laser(BaseModelPlus):
    """
    A object to control the state of the laser
    """
    on: Optional[bool] = None
    constant_power: Optional[float] = None
    dynamic_power: Optional[float] = None
    cutting_speed: Optional[float] = None
    travel_speed: Optional[float] = None
    spotsize: Optional[float] = None

    def get_dummy_objects(self):
        'create pseudo objects (for desktop 3D printing FullControl) based on laser parameters'
        dummy_objects = []
        if self.on != None:
            dummy_objects.append(Extruder(on=self.on))
        if self.constant_power != None:
            dummy_objects.append(ManualGcode(text=f'M3 S{self.constant_power:.1f}'))
        if self.dynamic_power != None:
            dummy_objects.append(ManualGcode(text=f'M4 S{self.dynamic_power:.1f}'))
        if self.cutting_speed != None:
            dummy_objects.append(Printer(print_speed=self.cutting_speed))
        if self.travel_speed != None:
            dummy_objects.append(Printer(travel_speed=self.travel_speed))
        if self.spotsize != None:
            dummy_objects.append(ExtrusionGeometry(width=self.spotsize))
        return dummy_objects


    def gcode(self, state):
        dummy_objects = self.get_dummy_objects()
        # call gcode function for each dummy object and record gcode to array
        gcode = [dummy_object.gcode(state) for dummy_object in dummy_objects]
        # remove None values from array
        gcode = [item for item in gcode if item is not None]
        # return gcode as string if gcode was returned
        if len(gcode) > 0: return('\n'.join(gcode))

    def visualize(self, state, plot_data, plot_controls):
        dummy_objects = self.get_dummy_objects()
        # call visualize function for each dummy object
        [dummy_object.visualize(state, plot_data, plot_controls) for dummy_object in dummy_objects]
    
