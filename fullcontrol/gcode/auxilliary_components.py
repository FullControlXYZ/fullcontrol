from typing import Optional
from fullcontrol.common import Fan as BaseFan
from fullcontrol.common import Hotend as BaseHotend
from fullcontrol.common import Buildplate as BaseBuildplate


class Fan(BaseFan):
    'Extend generic class with gcode method to convert the object to gcode'

    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        if self.speed_percent != None:
            return f'M106 S{int(self.speed_percent*255/100)} ; set fan speed'


class Hotend(BaseHotend):
    'Extend generic class with gcode method to convert the object to gcode'

    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        if self.tool == None:
            return f'M104 S{self.temp} ; set hotend temp and continue' if self.wait == False else f'M109 S{self.temp}  ; set hotend temp and wait'
        else:
            return f'M104 S{self.temp} T{self.tool} ; set hotend temp for tool {self.tool} and continue' if self.wait == False else f'M109 S{self.temp} T{self.tool} ; set hotend temp for tool {self.tool} and wait'


class Buildplate(BaseBuildplate):
    'Extend generic class with gcode method to convert the object to gcode'

    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        return f'M140 S{self.temp} ; set bed temp and continue' if self.wait == False else f'M190 S{self.temp} ; set bed temp and wait'
