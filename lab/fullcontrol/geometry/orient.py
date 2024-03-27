
from fullcontrol import Point, point_to_polar
from math import degrees


def constant_polar_angle_with_c(points: list, centre: Point, initial_c: float = 0):
  '''adjust c rotation for a list of points to ensure all points are rotated (by c) to have the same 
  polar angle in the XY plane relative to the centre point. Set initial_c (degreed) to adjust the 
  desired initial orientation
  '''
  complete_loops = 0
  inital_point_polar_angle = degrees(point_to_polar(points[0], centre).angle)
  polar_angle_previous = inital_point_polar_angle
  for i in range(len(points)):
    polar_angle_now = degrees(point_to_polar(points[i], centre).angle)
    if polar_angle_now < polar_angle_previous:
      complete_loops += 1
    c_beyond_first_point = (
        polar_angle_now - inital_point_polar_angle) + (complete_loops * 360)
    # negative because whatever polar angle the point is at needs to be offset by opposite C rotation
    points[i].c = initial_c-c_beyond_first_point
    polar_angle_previous = polar_angle_now
  return points
