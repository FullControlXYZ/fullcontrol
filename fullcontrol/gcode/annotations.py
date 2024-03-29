from typing import Optional
from pydantic import BaseModel


class GcodeComment(BaseModel):
    '''
    Represents a comment in a line of Gcode.

    Attributes:
        text (Optional[str]): The comment to be added as a new line of Gcode.
        end_of_previous_line_text (Optional[str]): The comment to be added at the end of the previous line of Gcode.
    '''

    text: Optional[str] = None
    end_of_previous_line_text: Optional[str] = None

    def gcode(self, state):
        '''
        Process this instance in a list of steps supplied by the designer to generate and return a line of Gcode.

        Args:
            state: The current state of the Gcode generation process.

        Returns:
            str: The generated line of Gcode.
        '''
        if self.end_of_previous_line_text != None:
            state.gcode[-1] += ' ; ' + self.end_of_previous_line_text
        if self.text != None:
            return '; ' + self.text
