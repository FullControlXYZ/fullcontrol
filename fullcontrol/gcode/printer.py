from typing import Optional
from fullcontrol.common import Printer as BasePrinter
# from fullcontrol.common import MultitoolPrinter as BaseMultitoolPrinter


class Printer(BasePrinter):
    '''
    A class representing a 3D printer.

    Attributes:
        command_list (Optional[dict]): A dictionary containing the printer's command list.
        new_command (Optional[dict]): A dictionary containing a new command to be added to the command list.
        speed_changed (Optional[bool]): A flag indicating whether the print speed or travel speed has changed.

    Methods:
        f_gcode(state): Generates and returns a line of gcode based on the current state of the printer.
        gcode(state): Processes the printer instance and generates a line of gcode based on the supplied list of steps.

    See the documentation for more information about other attributes.
    '''
    command_list: Optional[dict] = None
    new_command: Optional[dict] = None
    speed_changed: Optional[bool] = None

    def f_gcode(self, state):
        """
        Generate the G-code for the feedrate (F) based on the current state.

        Parameters:
        - state: The current state of the printer.

        Returns:
        - The G-code string for the feedrate (F) based on the current state.
        """
        if self.speed_changed == True:
            return f'F{self.print_speed} ' if state.extruder.on else f'F{self.travel_speed} '
        else:
            return ''

    def gcode(self, state):
        '''
        Process this instance in a list of steps supplied by the designer to generate and return a line of gcode.

        Args:
            state: The state object containing information about the printer's current state.

        Returns:
            A line of gcode generated based on the supplied steps.

        '''
        # update all attributes of the tracking instance with the new instance (self)
        state.printer.update_from(self)
        if self.print_speed != None \
                or self.travel_speed != None:
            state.printer.speed_changed = True
        if self.new_command != None:
            state.printer.command_list = {**state.printer.command_list, **self.new_command}
