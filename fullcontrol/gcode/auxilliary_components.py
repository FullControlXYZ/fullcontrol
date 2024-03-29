from typing import Optional
from fullcontrol.common import Fan as BaseFan
from fullcontrol.common import Hotend as BaseHotend
from fullcontrol.common import Buildplate as BaseBuildplate


class Fan(BaseFan):
    '''
    A generic Fan with gcode method added.

    This class represents a generic fan component and provides a method to generate a line of gcode based on its state.

    Attributes:
        speed_percent (float): The speed of the fan as a percentage (0-100).

    Methods:
        gcode(state): Process this instance in a list of steps supplied by the designer to generate and return a line of gcode.
    '''
    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        if self.speed_percent != None:
            return f'M106 S{int(self.speed_percent*255/100)} ; set fan speed'


class Hotend(BaseHotend):
    '''
    A class representing a generic hotend with gcode method added.

    Attributes:
        tool (int): The tool number associated with the hotend.
        temp (int): The temperature of the hotend.
        wait (bool): A flag indicating whether to wait for the hotend to reach the desired temperature.

    Methods:
        gcode(state): Process this instance in a list of steps supplied by the designer to generate and return a line of gcode.
    '''
    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        if self.tool == None:
            return f'M104 S{self.temp} ; set hotend temp and continue' if self.wait == False else f'M109 S{self.temp}  ; set hotend temp and wait'
        else:
            return f'M104 S{self.temp} T{self.tool} ; set hotend temp for tool {self.tool} and continue' if self.wait == False else f'M109 S{self.temp} T{self.tool} ; set hotend temp for tool {self.tool} and wait'


class Buildplate(BaseBuildplate):
    '''
    A generic BuildPlate with gcode method added.

    This class represents a build plate used in 3D printing. It inherits from the BaseBuildplate class.

    Attributes:
        temp (int): The temperature of the build plate.
        wait (bool): A flag indicating whether to wait for the build plate to reach the desired temperature.

    Methods:
        gcode(state): Process this instance in a list of steps supplied by the designer to generate and return a line of gcode.
    '''
    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        return f'M140 S{self.temp} ; set bed temp and continue' if self.wait == False else f'M190 S{self.temp} ; set bed temp and wait'
