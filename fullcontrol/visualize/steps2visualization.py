
from fullcontrol.visualize.state import State
from fullcontrol.visualize.plot_data import PlotData
from fullcontrol.visualize.controls import PlotControls
from fullcontrol.visualize.tips import tips


def visualize(steps: list, plot_controls: PlotControls, show_tips: bool):
    '''
    Visualize the list of steps.

    Parameters:
    - steps (list): The list of steps to visualize.
    - plot_controls (PlotControls, optional): The style of the plot can be adjusted by passing a PlotControls instance.

    Returns:
    - plot_data (PlotData): The plot data if `plot_controls.raw_data` is True, otherwise None.
    '''
    plot_controls.initialize()
    if show_tips: tips(plot_controls)

    state = State(steps, plot_controls)
    plot_data = PlotData(steps, state)
    for step in steps:
        step.visualize(state, plot_data, plot_controls)
    plot_data.cleanup()

    if plot_controls.raw_data == True:
        return plot_data
    else:
        from fullcontrol.visualize.plotly import plot
        plot(plot_data, plot_controls)
