from typing import Optional, Any
from fullcontrol.common import BaseModelPlus
from math import pi


class ExtrusionGeometry(BaseModelPlus):
    '''Geometric description of the printed extrudate.
    
    The 'area_model' is used to specify how the cross-sectional area of the extrudate is defined. The available
    options for 'area_model' are: rectangle (requires width and height), stadium (requires width and height),
    circle (requires diameter), and manual (requires area attribute to be set manually). The 'area' attribute is
    automatically calculated unless 'area_model' is set to 'manual'.
    '''
    # area_model options: 'rectangle' / 'stadium' / 'circle' / 'manual':
    area_model: Optional[str] = None
    # width of printed line for area_model = rectangle or stadium:
    width: Optional[float] = None
    # height of printed line for area_model = rectangle or stadium:
    height: Optional[float] = None
    # diameter of printed line for area_model = circle:
    diameter: Optional[float] = None
    # automatically calculated based on area_model and relevant attributes
    area: Optional[float] = None

    def update_area(self) -> float:
        '''Update the area attribute based on the area_model and relevant attributes.'''
        if self.area_model == "rectangle":
            self.area = self.width * self.height
        elif self.area_model == "stadium":
            self.area = ((self.width - self.height) * self.height) + (pi * (self.height / 2) ** 2)
        elif self.area_model == "circle":
            self.area = (pi * (self.diameter / 2) ** 2)
        elif self.area_model == "manual":
            pass


class StationaryExtrusion(BaseModelPlus):
    """
    Represents stationary extrusion in a 3D printer.

    This class is used to manage and control the extrusion of a specific volume of material at a set speed while the printer's nozzle is stationary. Negative volumes indicate retraction.

    Attributes:
        volume (float): The volume of material to extrude. Negative values indicate retraction.
        speed (int): The speed at which to extrude the material - the units depend on the gcode format used but are typically mm/min.
    """

    # design attributes to control one-off extrusion without nozzle movement:
    volume: float
    speed: int


class Extruder(BaseModelPlus):
    """Represents an extruder for controlling extrusion.

    Attributes:
        on (bool, optional): Indicates whether extrusion is on or off.
    """
    on: Optional[bool] = None
