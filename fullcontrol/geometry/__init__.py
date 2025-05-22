
# import classes
from fullcontrol.combinations.gcode_and_visualize.classes import Point, Extruder
# objects are imported here with functionality for both gcode and visualization. this means
# the modules within the geometry subpackage can simply import from here, with the idea being
# that only one import command needs to be changed if a different combination of properties is
# used (i.e. this bit in the line above: fullcontrol.combinations.gcode_and_visualize.classes).
from fullcontrol.geometry.vector import Vector
from fullcontrol.geometry.polar import PolarPoint

# import functions
from fullcontrol.geometry.polar import point_to_polar, polar_to_point, polar_to_vector
from fullcontrol.geometry.midpoint import midpoint, interpolated_point, centreXY_3pt
# , distance_forgiving
from fullcontrol.geometry.measure import distance, angleXY_between_3_points, path_length
from fullcontrol.geometry.move import move
from fullcontrol.geometry.move_polar import move_polar
from fullcontrol.geometry.reflect import reflectXY, reflectXY_mc
from fullcontrol.geometry.reflect_polar import reflectXYpolar
from fullcontrol.geometry.ramping import ramp_xyz, ramp_polar
from fullcontrol.geometry.arcs import arcXY, variable_arcXY, elliptical_arcXY, arcXY_3pt
from fullcontrol.geometry.shapes import rectangleXY, circleXY, circleXY_3pt, ellipseXY, polygonXY, spiralXY, helixZ
from fullcontrol.geometry.waves import squarewaveXY, squarewaveXYpolar, trianglewaveXYpolar, sinewaveXYpolar
from fullcontrol.geometry.segmentation import segmented_line, segmented_path
from fullcontrol.geometry.travel_to import travel_to
