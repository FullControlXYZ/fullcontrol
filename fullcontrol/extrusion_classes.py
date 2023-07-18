from typing import Optional, Any
from fullcontrol.common import BaseModelPlus
from math import pi


class ExtrusionGeometry(BaseModelPlus):
    ''' geometric description of the printed extrudate. 'area_model' is used to specify how cross-sectional
    area of the extrudate is defined. area_model options: rectangle (requires width and height) / stadium 
    (requires width and height) / circle (requires diameter) / manual (requires area attribute to be set
    manually). the 'area' attribute is automatically calculated unless area_model=='manual' 
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
        if self.area_model == "rectangle":
            self.area = self.width*self.height
        elif self.area_model == "stadium":
            self.area = ((self.width-self.height)*self.height)+(pi*(self.height/2)**2)
        elif self.area_model == "circle":
            self.area = (pi*(self.diameter/2)**2)
        elif self.area_model == "manual":
            pass


class StationaryExtrusion(BaseModelPlus):
    'extrude a set volume of material at the set speed while the nozzle is stationary. negative volumes indicate retraction'
    # design attributes to control one-off extrusion without nozzle movement:
    volume: float
    speed: int


class Extruder(BaseModelPlus):
    'control whether extrusion is on or off'
    on: Optional[bool] = None
