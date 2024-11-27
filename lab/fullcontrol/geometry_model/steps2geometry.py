from fullcontrol.visualize.plot_data import PlotData
from lab.fullcontrol.geometry_model.controls import ModelControls
from fullcontrol.visualize.controls import PlotControls
from fullcontrol.visualize.plotly import generate_mesh

def generate_stl(data: PlotData, controls: ModelControls):
    from fullcontrol.visualize.tube_mesh import CylindersMesh, FlowTubeMesh, MeshExporter

    sides, rounding_strength, flat_sides = controls.shape_properties()
    Mesh = {'flow': FlowTubeMesh, 'cylinders': CylindersMesh}[controls.tube_type]
    meshes = []
    for path in data.paths:
        if path.extruder.on:
            meshes.append(
                generate_mesh(path, 0, Mesh, sides, rounding_strength, flat_sides)
            )

    binary_file = controls.stl_type.lower() == 'binary'
    MeshExporter({'name': 'extrusion'}, meshes).to_stl(
        controls.stl_filename, binary_file, combined_file=controls.stls_combined, overwrite=True
    )

def reuse_visualize(steps: list, model_controls: ModelControls):
    from fullcontrol.visualize.state import State

    plot_controls = PlotControls(tube_type=model_controls.tube_type,
                                 initialization_data=model_controls.initialization_data)
    state = State(steps, plot_controls)
    plot_data = PlotData(steps, state)
    for step in steps:
        step.visualize(state, plot_data, plot_controls)
    plot_data.cleanup()
    return plot_data

def geometry_model(steps: list, model_controls: ModelControls):
    ''' use the existing visualize function to get plot_data that is normally used to generate 
    the 3D model for visualization and is used here to generate the 3D model for stl output or similar
    '''
    from datetime import datetime

    plot_data = reuse_visualize(steps, model_controls)
    model_controls.stl_filename += '.stl' if not model_controls.include_date \
        else datetime.now().strftime("__%d-%m-%Y__%H-%M-%S.stl")
    generate_stl(plot_data, model_controls)

    print("stl file created. remember to set ModelControls(tube_type='cylinders') for more accurate widths/heights but a less-smooth model than ModelControls(tube_type='flow') (default)")
