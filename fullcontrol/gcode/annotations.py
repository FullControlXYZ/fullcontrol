from typing import Optional
from pydantic import BaseModel


class GcodeComment(BaseModel):
    '''use the 'text' attribute to add a comment as a new line gcode. use the 'end_of_previous_line_text' attribute 
    to add a comment to the end of the line of gcode produced by the previous step'''
    text: Optional[str] = None
    end_of_previous_line_text: Optional[str] = None

    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        if self.end_of_previous_line_text != None:
            state.gcode[-1] += ' ; ' + self.end_of_previous_line_text
        if self.text != None:
            return '; ' + self.text
