from typing import Optional
from fullcontrol.common import BaseModelPlus


class Fan(BaseModelPlus):
    'fan speed percent (0-100)'
    speed_percent: Optional[int] = None


class Hotend(BaseModelPlus):
    '''set temperature of hotend. if wait==True, system will wait for temperature to be reached
    before continuing. tool number can be defined for multi-tool printers
    '''
    temp: Optional[int] = None
    wait: Optional[bool] = False
    tool: Optional[int] = None


class Buildplate(BaseModelPlus):
    'set temperature of the buildplate. if wait==True, system will wait for temperature to be reached before continuing'
    temp: Optional[int] = None
    wait: Optional[bool] = False
