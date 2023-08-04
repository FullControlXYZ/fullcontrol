
from typing import Optional
from fullcontrol.common import BaseModelPlus


class PrinterCommand(BaseModelPlus):
    'state the id of the printer command that should be executed ... manifesting in an appropriate line of gcode'
    id: Optional[str] = None

    def gcode(self, state):
        # this type of command can only be used after a Printer instance with commandlist has updated state.printer
        return state.printer.command_list[self.id]


class ManualGcode(BaseModelPlus):
    "custom gcode defined by 'text' attribute will be added as a new line of gcode"
    text: Optional[str] = None

    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        if self.text != None:
            return self.text
