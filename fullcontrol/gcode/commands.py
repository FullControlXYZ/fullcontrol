
from typing import Optional
from fullcontrol.common import BaseModelPlus


class PrinterCommand(BaseModelPlus):
    """
    Represents a printer command that should be executed, manifesting in an appropriate line of gcode.

    Attributes:
        id (Optional[str]): The ID of the printer command that should be executed.
    """

    id: Optional[str] = None

    def gcode(self, state):
        """
        Returns the gcode representation of the printer command.

        Args:
            state: The current state of the printer.

        Returns:
            str: The gcode representation of the printer command.
        """
        # this type of command can only be used after a Printer instance with commandlist has updated state.printer
        return state.printer.command_list[self.id]


class ManualGcode(BaseModelPlus):
    """
    Represents custom gcode defined by the 'text' attribute.
    
    Attributes:
        text (Optional[str]): The custom gcode text to be added as a new line of gcode.
    """
    text: Optional[str] = None

    def gcode(self, state):
        """
        Process this instance in a list of steps supplied by the designer to generate and return a line of gcode.
        
        Args:
            state: The current state of the gcode generation process.
        
        Returns:
            str: The generated line of gcode.
        """
        if self.text != None:
            return self.text
