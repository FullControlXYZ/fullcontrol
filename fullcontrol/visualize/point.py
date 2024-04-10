from typing import Optional, TYPE_CHECKING
from fullcontrol.point import Point as BasePoint
from random import random
from fullcontrol.visualize.bounding_box import BoundingBox
from math import cos, sin, tau
from fullcontrol.visualize.controls import PlotControls

if TYPE_CHECKING:
    from fullcontrol.visualize.state import State
    from fullcontrol.visualize.plot_data import PlotData


class Point(BasePoint):
    '''
    A generic fullcontrol Point with a color attribute and color/visualization methods added.

    Attributes:
        color (Optional[list]): The color of the point in RGB format [r, g, b] with values 0-1.
    '''

    color: Optional[list] = None  # [r,g,b]

    def visualize(self, state: 'State', plot_data: 'PlotData', plot_controls: PlotControls):
        '''
        Process a Point in a list of steps supplied by the designer to update plot_data and state.

        Args:
            state ('State'): The current state of the plot.
            plot_data ('PlotData'): The data used for plotting.
            plot_controls ('PlotControls'): The controls for plotting.

        Returns:
            None
        '''

        change_check = False
        precision_xyz = 3  # number of decimal places to use for x y z values in plot_data
        if self.x != None and self.x != state.point.x:
            state.point.x = round(self.x, precision_xyz)
            change_check = True
        if self.y != None and self.y != state.point.y:
            state.point.y = round(self.y, precision_xyz)
            change_check = True
        if self.z != None and self.z != state.point.z:
            state.point.z = round(self.z, precision_xyz)
            change_check = True
        if self.color != None and self.color != state.point.color:
            state.point.color = self.color
            change_check = True
        if change_check:
            state.point.update_color(state, plot_data, plot_controls)
            plot_data.paths[-1].add_point(state)
            state.point_count_now += 1

    def update_color(self, state: 'State', plot_data: 'PlotData', plot_controls: 'PlotControls'):
        '''
        Update the color attribute of this point with [R, G, B] based on the color_type specified in plot_controls.

        Args:
            state ('State'): The current state of the plot.
            plot_data ('PlotData'): The data used for plotting.
            plot_controls ('PlotControls'): The controls for plotting.

        Returns:
            None
        '''

        precision_color = 3  # number of decimal places to use for colors in plot_data

        def travel():
            return [0.75, 0.5, 0.5]

        def random_blue():
            return [0.1, round(random(), precision_color), 2]

        def z_gradient(point: Point, bounding_box: BoundingBox):
            z_range = max(bounding_box.rangez, 0.00000001)
            # round to the same number of decimal places used for xyz ('precision_xyz') to avoid numerical rounding errors causing negative or very large (not allowbale) values in plot_data
            z_min = round(bounding_box.minz, 3)
            return [0, round((point.z-z_min)/z_range, precision_color), 1]

        def print_sequence(point_count_now: int, point_count_total: int):
            return [round(0.8*max(1-(2*point_count_now/point_count_total), 0), precision_color), round(max((2*point_count_now/point_count_total)-1, 0), precision_color), 1]

        def print_sequence_fluctuating(point_count_now: int, point_count_total: int, fluctuations: int):
            point_count_fluc = point_count_total / fluctuations
            return [round(0.25+0.25*sin((((point_count_now % point_count_fluc)+0.00001)/point_count_fluc)*tau), precision_color),
                    round(0.5-0.5*cos((((point_count_now % point_count_fluc)+0.00001)/point_count_fluc)*tau), precision_color),
                    1]

        if plot_controls.color_type == 'manual':
            pass
        else:
            if state.extruder.on == True:
                if plot_controls.color_type == 'random_blue':
                    self.color = random_blue()
                elif plot_controls.color_type == 'z_gradient':
                    self.color = z_gradient(state.point, plot_data.bounding_box)
                elif plot_controls.color_type == 'print_sequence':
                    self.color = print_sequence(state.point_count_now, state.point_count_total)
                elif plot_controls.color_type == 'print_sequence_fluctuating':
                    self.color = print_sequence_fluctuating(state.point_count_now, state.point_count_total, 5)
                else:
                    raise Exception(f'colour {plot_controls.color_type} not in list of allowable color types')
            else:
                self.color = travel()
