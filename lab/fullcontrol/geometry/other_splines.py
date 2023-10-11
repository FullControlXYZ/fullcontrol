from lab.fullcontrol.geometry import Point


def catmull_rom_spline(control_points, num_points=10, tension=0.5):
    '''return a list of points following a catmull-rom spline that passes through the control
    points. control the smoothness with tension (higher value is smoother - e.g. 0.5). 
    '''
    interpolated_points = []  # List to store the interpolated points

    num_segments = len(control_points) - 1

    segments_per_control_point = max(2, int(num_points/num_segments))
    for i in range(num_segments):
        # Select the control points for this segment
        p0, p1, p2, p3 = control_points[max(0, i - 1)], control_points[i], control_points[i + 1], control_points[min(i + 2, num_segments)]

        # Generate interpolated points for this segment
        for t in range(segments_per_control_point + 1):
            t_normalized = t / segments_per_control_point

            # Calculate blending coefficients
            t2 = t_normalized * t_normalized
            t3 = t2 * t_normalized

            c0 = -tension * t3 + 2 * tension * t2 - tension * t_normalized
            c1 = (2 - tension) * t3 + (tension - 3) * t2 + 1
            c2 = (tension - 2) * t3 + (3 - 2 * tension) * t2 + tension * t_normalized
            c3 = tension * t3 - tension * t2

            # Interpolate the point on the curve using the control points and coefficients
            interpolated_point = Point(
                x=c0 * p0.x + c1 * p1.x + c2 * p2.x + c3 * p3.x,
                y=c0 * p0.y + c1 * p1.y + c2 * p2.y + c3 * p3.y,
                z=c0 * p0.z + c1 * p1.z + c2 * p2.z + c3 * p3.z
            )

            interpolated_points.append(interpolated_point)

    return interpolated_points
