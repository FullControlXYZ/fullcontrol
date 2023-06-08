
from fullcontrol.visualize.state import State
from fullcontrol.visualize.plot_data import PlotData
from fullcontrol.visualize.controls import PlotControls


def visualize(steps: list, plot_controls: PlotControls = PlotControls()):
    'visualize the list of steps. optionally, the style of the plot can be adjusted by passing a PlotControls instance'
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
