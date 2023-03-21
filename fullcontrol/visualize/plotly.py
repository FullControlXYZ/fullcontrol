
import plotly.graph_objects as go
from fullcontrol.visualize.plot_data import PlotData
from fullcontrol.visualize.controls import PlotControls


def plot(data: PlotData, controls: PlotControls):
    'plot data for x y z lines with RGB colors and annotations. style of plot governed by controls'
    fig = go.Figure()

    def column(matrix: list, i: int):
        'return list of ith elements from a 2D array'
        return [row[i] for row in matrix]

    # generate line plots
    path_count = len(data.paths)
    for i in range(path_count):
        line_point_count = len(data.paths[i].xvals)
        colors_now = []
        for j in range(line_point_count):
            colors_now.append(
                f'rgb({data.paths[i].colors[j][0]*255:.2f}, {data.paths[i].colors[j][1]*255:.2f}, {data.paths[i].colors[j][2]*255:.2f})')
        linewidth_now = controls.line_width * \
            2 if data.paths[i].extruder.on == True else controls.line_width*0.5
        if not controls.hide_travel or data.paths[i].extruder.on == True:
            fig.add_trace(go.Scatter3d(mode='lines', x=data.paths[i].xvals, y=data.paths[i].yvals,
                          z=data.paths[i].zvals, showlegend=False, line=dict(width=linewidth_now, color=colors_now)))

    # find a bounding box, to create a plot with equally proportioned X Y Z scales (so a cuboid looks like a cuboid, not a cube)
    bounding_box_size = max(data.bounding_box.maxx-data.bounding_box.minx, data.bounding_box.maxy -
                            data.bounding_box.miny, data.bounding_box.maxz-min(0, data.bounding_box.minz))
    bounding_box_size += 0.002

    # generate annotations
    annotations_count = len(data.annotations)
    annotations_pts = []
    annotations = []
    if controls.hide_annotations == False and not controls.neat_for_publishing:
        for i in range(annotations_count):
            annotations_pts.append(
                [data.annotations[i]['x'], data.annotations[i]['y'], data.annotations[i]['z']])
            annotations.append(dict(
                showarrow=False,
                x=annotations_pts[i][0],
                y=annotations_pts[i][1],
                z=annotations_pts[i][2],
                text=data.annotations[i]['label'],
                yshift=10))
        fig.add_trace(go.Scatter3d(mode='markers', x=column(annotations_pts, 0), y=column(
            annotations_pts, 1), z=column(annotations_pts, 2), showlegend=False, marker=dict(size=2, color='red')))

        # make sure the bounding box is big enough for the annotations
        # the 0.001 is to make sure the annotations don't lie on the boundary
        for i in range(annotations_count):
            if annotations_pts[i][0] < data.bounding_box.midx-bounding_box_size/2+0.001:
                bounding_box_size = 2 * \
                    (data.bounding_box.midx-annotations_pts[i][0])+0.002
            if annotations_pts[i][0] > data.bounding_box.midx+bounding_box_size/2-0.001:
                bounding_box_size = 2 * \
                    (annotations_pts[i][0]-data.bounding_box.midx)+0.002
            if annotations_pts[i][1] < data.bounding_box.midy-bounding_box_size/2+0.001:
                bounding_box_size = 2 * \
                    (data.bounding_box.midy-annotations_pts[i][1])+0.002
            if annotations_pts[i][1] > data.bounding_box.midy+bounding_box_size/2-0.001:
                bounding_box_size = 2 * \
                    (annotations_pts[i][1]-data.bounding_box.midy)+0.002
            if annotations_pts[i][2] < data.bounding_box.midz-bounding_box_size/2+0.001:
                bounding_box_size = 2 * \
                    (data.bounding_box.midz-annotations_pts[i][2])+0.002
            if annotations_pts[i][2] > data.bounding_box.midz+bounding_box_size/2-0.001:
                bounding_box_size = 2 * \
                    (annotations_pts[i][2]-data.bounding_box.midz)+0.002

    camera = dict(eye=dict(x=-0.5/controls.zoom, y=-1/controls.zoom, z=-0.5+0.5/controls.zoom),
                  center=dict(x=0, y=0, z=-0.5))
    fig.update_layout(template='plotly_dark', paper_bgcolor="black", scene_aspectmode='cube', scene=dict(annotations=annotations,
                                                                                                         xaxis=dict(backgroundcolor="black", nticks=10, range=[
                                                                                                                    data.bounding_box.midx-bounding_box_size/2, data.bounding_box.midx+bounding_box_size/2],),
                                                                                                         yaxis=dict(backgroundcolor="black", nticks=10, range=[
                                                                                                             data.bounding_box.midy-bounding_box_size/2, data.bounding_box.midy+bounding_box_size/2],),
                                                                                                         zaxis=dict(backgroundcolor="black", nticks=10, range=[min(0, data.bounding_box.minz), bounding_box_size],),),
                      scene_camera=camera,
                      width=800, height=500, margin=dict(l=10, r=10, b=10, t=10, pad=4))
    if controls.hide_axes or controls.neat_for_publishing:
        for axis in ['xaxis', 'yaxis', 'zaxis']:
            fig.update_layout(
                scene={axis: dict(showgrid=False, zeroline=False, visible=False)})
    if controls.neat_for_publishing:
        fig.update_layout(width=500, height=500)
    fig.show()
