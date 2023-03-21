
from fullcontrol.combinations.gcode_and_visualize.classes import Point, ExtrusionGeometry, Printer
from fullcontrol.geometry import midpoint, distance, point_to_polar, segmented_line
from fullcontrol.common import flatten
from math import cos, pi

# these functions allow streamline-slicing - see method images and case study in this journal paper:
# https://www.researchgate.net/publication/346098541


def make_grid(path1: list, path2: list, cells_between: int) -> list:
    'create a grid of points by interpolating between the points in the two supplied paths'
    return [segmented_line(path1[i], path2[i], cells_between) for i in range(len(path1))]


def convex_segment(a1: Point, a2: Point, b1: Point, b2: Point) -> list:
    ''' identify the start/end coordinates and 'extrusion width' of a line that fills a region defined by four corners. the
    line goes from the midpoint of points a1 and a2 to the midpoint of points b1 and b2. since a single extrusion width is 
    used for the whole line (printed by one GCode command) a single average 'extrusion width' is calulated. returns a list 
    of an ExtrusionGeometry (extrusion width) and two Points for the start and end of each line
    '''
    mid_a = midpoint(a1, a2)  # start point of line
    mid_b = midpoint(b1, b2)  # end point of line
    mid_1 = midpoint(a1, b1)  # mid point of one edge of the line
    mid_2 = midpoint(a2, b2)  # mid point of other edge of the line
    # this width is NOT normal to the line direction so needs adjustment based on skew
    mid_width = distance(mid_1, mid_2)
    skew = point_to_polar(mid_a, mid_b).angle - (point_to_polar(mid_1, mid_2).angle - pi/2)
    # the absolute value is used since it means the "- pi/2" can be used to calculate skew regardless of line directions
    line_width = mid_width * abs(cos(skew))
    # this function has been checked by comparing the area calculated from returned line_width*line_length to that calculated for vertices a1/a2/b1/b2 here: https://www.omnicalculator.com/math/quadrilateral
    return [ExtrusionGeometry(width=line_width), mid_a, mid_b]


def convex_from_grid(points_grid: list) -> list:
    ''' create a list of steps to print the necessary lines of the necessary width to fill all the cells in a grid (printing line by line)
    '''
    steplist = []
    # j represents one of the lines being printed
    for j in range(len(points_grid[0])-1):
        # i runs through the segments of each line
        for i in range(len(points_grid)-1):
            steplist.append(convex_segment(points_grid[i][j], points_grid[i][j+1], points_grid[i+1][j], points_grid[i+1][j+1]))
    return steplist


def convex_segment_and_speed(a1: Point, a2: Point, b1: Point, b2: Point, speed_ref: float, width_ref: float) -> list:
    ''' identify the start/end coordinates and 'extrusion width' of a line that fills a region defined by four corners. the
    line goes from the midpoint of points a1 and a2 to the midpoint of points b1 and b2. since a single extrusion width is 
    used for the whole line (printed by one GCode command) a single average 'extrusion width' is calulated. returns a list 
    of an Extruder (extrusion width) and two Points for the start and end of the line. Max speeds are capped to 10x speed_ref
    '''
    mid_a = midpoint(a1, a2)  # start point of line
    mid_b = midpoint(b1, b2)  # end point of line
    mid_1 = midpoint(a1, b1)  # mid point of one edge of the line
    mid_2 = midpoint(a2, b2)  # mid point of other edge of the line
    # this width is NOT normal to the line direction so needs adjustment based on skew
    mid_width = distance(mid_1, mid_2)
    skew = point_to_polar(mid_a, mid_b).angle - \
        (point_to_polar(mid_1, mid_2).angle - pi/2)
    # the absolute value is used since it means the "- pi/2" can be used to calculate skew regardless of line directions
    line_width = mid_width * abs(cos(skew))
    speed = speed_ref*(width_ref/line_width)
    speed = min(speed, speed_ref*10)
    # this function has been checked by comparing the area calculated from returned line_width*line_length to that calculated for vertices a1/a2/b1/b2 here: https://www.omnicalculator.com/math/quadrilateral
    return [ExtrusionGeometry(width=line_width), Printer(print_speed=speed), mid_a, mid_b]


def convex_from_grid_and_speed(points_grid: list, speed_ref: float, width_ref: float) -> list:
    ''' same as convex_from_grid() but also calculates what speed should be used for each segement to maintain a constant
    volumetric flow rate (dictated by the reference speed and width supplied by the user)
    '''
    steplist = []
    # j represents one of the lines being printed
    for j in range(len(points_grid[0])-1):
        # i runs through the segments of each line
        for i in range(len(points_grid)-1):
            steplist.append(convex_segment_and_speed(
                points_grid[i][j], points_grid[i][j+1], points_grid[i+1][j], points_grid[i+1][j+1], speed_ref, width_ref))
    return steplist


def convex_pathsXY(path1: list, path2: list, lines: int, vary_speed: bool = False, speed_ref: float = None, width_ref: float = None) -> list:
    ''' generate a series of paths to fill the space between supplied path1 and path2 with 
    streamlined lines of continuously varying extrusion width. the points in each path are
    directly interpolated between. if vary_speed=True, the reference speed and extrusion 
    width must be supplied, and the speed of the nozzle will continuously vary to maintain 
    contant volumetric flowrate. see https://www.researchgate.net/publication/346098541
    '''
    points_grid = make_grid(path1, path2, lines)
    if vary_speed == False:
        steplist = convex_from_grid(points_grid)
    else:
        if speed_ref == None:
            raise ValueError("parameter speed_ref must be supplied")
        if width_ref == None:
            raise ValueError("parameter width_ref must be supplied")
        steplist = convex_from_grid_and_speed(points_grid, speed_ref, width_ref)
    return flatten(steplist)
