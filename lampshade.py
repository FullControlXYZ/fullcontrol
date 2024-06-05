# @title **Lampshade Design** { display-mode: "form"}

# @markdown #### **🡸 Click ▶︎ button to connect to python** --- *connection may take ~20 seconds*
# @markdown  #### **🡸 Click it again** to regenerate the design after changing parameters **(or press *`shift + enter`)*** --- *gcode generation may take ~20 seconds*

# import python packages (if not already imported)
import sys
if 'fullcontrol' not in sys.modules:
  !pip install git+https://github.com/FullControlXYZ/fullcontrol --quiet
  import fullcontrol as fc
  import lab.fullcontrol as fclab
  from google.colab import files
  from math import tau, sin, cos, exp, pi

# output type (widget)
# @markdown ---
# @markdown ### **Controls:**
Output = 'GCode' # @param ["Simple Plot", "Detailed Plot", "GCode"]
target = 'visualize' if Output in ['Detailed Plot', 'Simple Plot'] else 'gcode' # 'visualize' or 'gcode'
Annotations = True # @param {type:"boolean"}


# setup printer parameters
# @markdown ### **Printer parameters:**
Printer_name = 'bambulab_x1' # @param ['generic', 'ultimaker2plus', 'prusa_i3',  'ender_3', 'cr_10', 'bambulab_x1', 'toolchanger_T']
Nozzle_temp = 230 # @param {type:"number"} # default 220
Bed_temp = 70 # @param {type:"number"} # default 40
Fan_percent = 40 # @param {type:"number"} # default 100
Material_flow_percent = 100 # @param {type:"number"} # default 100
Print_speed_percent = 300 # @param {type:"number"} # default 100
Design_name = 'fc_lampshade'

# design parameters (widgets)
# @markdown ### **Design parameters:**
Height = 160 # @param {type:"slider", min:100, max:200, step:5}
# default 150 # Overall height of the lampshade
Nominal_radius = 45 # @param {type:"slider", min:20, max:50, step:1}
# default 34 # Initial radius of teh shell before all the modifications like bulges
Tip_length = 30 # @param {type:"slider", min:10, max:30, step:2}
# default 20 # the extra radius to add to the initial radius for the pointy bits
Star_tips = 6 # @param {type:"slider", min:0, max:8, step:1}
# default 6 # Number of pointy star tips
Main_bulge = 25 # @param {type:"slider", min:0, max:25, step:2.5}
# default 22.5 # increase in radius to get an overall bulbous shape (wider half-way up than at top/bottom.
Secondary_bulges = 15 # @param {type:"slider", min:0, max:20, step:2.5}
# default 15 # increase in radius for the two bulges about 1/3 and 2.3 of the way up the overall height of the lampshade
Inner_frame_hole_diameter = 28 # @param {type:"slider", min:20, max:40, step:1}
# default 30 # Diameter of the inner ring of the inner frame - this is increased autoamtcially to allow for extrusion width
Inner_frame_height = 5 # @param {type:"slider", min:0, max:10, step:1}
# default 3 # Height the inner frame is printed
Inner_frame_wave_amplitude = 17.5 # @param {type:"number"}
# default 17.5 # This is the amplitude of the wave lines of the inner frame. To get neighbouring wavey lines to touch, this will need to be adjusted if the lengths of the lines changes.
Centre_XY = 110 # @param {type:"number"}
# default 105 # Centre of the lampshade on the print bed in XY
# automatically convert widget design parameters to variables used in the python design
height, r_0, tip_len, n_tip, bulge1, bulge2, frame_rad_inner, frame_height, amp_1, centre_xy = Height, Nominal_radius, Tip_length, Star_tips, Main_bulge, Secondary_bulges, Inner_frame_hole_diameter/2, Inner_frame_height, Inner_frame_wave_amplitude, Centre_XY

# advanced design parameters
# shell parameters:
zag_min, zag_max = 1, 5 # Depth of zigzags at the flat region of the shade zag_min (where they don't need to be deep to achieve a nice rippled texture because they are closer together (smaller radius)) and at the star tips zag_max (where they need to be deeper to still look look good deep ridges)
rip_depth, rip_freq = 0.5, 30 # Depth of tiny ripples in the Z direction and how many tiny ripples there are in the Z direction over the whole height
swerve = 0.02 # radians #  The swerving streamlines are achieved by angular offsets. This number controls the magnitude of those offsets and the amount of swerve.
segs_shell = 300 # Segments in the whole perimeter of the shell
x_1, x_2 = 6, 30 # These parameters controls how high up the shade the streamline swerves come into effect (and return to original shape at the top of the lampshade)
# inner-frame parameters:
frame_width_factor = 2.5 # The extrusion width of the inner frame is greater than the extrusion width of the outer shade by theis factor
frame_line_spacing_ratio = 0.2 # How laterally offset are the lines of the inner frame when they kiss (as a fraction of extrusion width) - the centre to centre distance of the lines is 2 * this value * frame line extrusion width
layer_ratio = 2 # this number is the number of layers of the shell that are printed for every layer of the frame
start_angle = 0.75*tau # this cannot be modified without also modifying the direction of the first frame line (currently in +Y direction)
frame_overlap =  2.5 # how much the inner frame overlaps with the shell
segs_frame = 64 # Segments per single wavey line in the inner frame
# printing parameters:
EH, EW = 0.2, 0.5 # Extrusion height and width for the shell of the lamp shade
initial_print_speed, main_print_speed, speedchange_layers  = 500, 1500, 5 # print speed ramps up from initial_print_speed to main_print_speed over the first few layers (speedchange_layers)


# automatically calculated parameters
frame_rad_max = r_0+tip_len+frame_overlap # Outer radius of the wavey lines of the inner frame - this value is set so the lines connect will with the outer shade section, but don't cross it too much
# centre_xy = frame_rad_max+bulge1+bulge2+tip_len-10
frame_rad_inner += EW/2 # increase the hole size to allow for the extrusion width
if Output == 'Simple Plot': EH, segs_shell = EH*30, n_tip*20
elif Output == 'Detailed Plot': EH = EH*10
total_segs = segs_shell*(height/EH)
shell_layers, frame_layers = int(height/EH), int(frame_height/EH)
initial_z = EH*0.7 # initial nozzle position is set lower than the extrusion height to get a bit of 'squish' for good bed adhesion

# generate design
steps = []
t_steps_shell, t_steps_frame_line = fc.linspace(0, 1, segs_shell+1), fc.linspace(0, 1, segs_frame+1)
for layer in range(shell_layers):
    if layer <= speedchange_layers: print_speed = initial_print_speed + (main_print_speed-initial_print_speed)*(layer/speedchange_layers)
    z_now = initial_z + layer*EH
    z_fraction = z_now/height
    centre_now = fc.Point(x=centre_xy, y=centre_xy, z=z_now)
    shell_steps, wave_steps = [], []
    for t_now in t_steps_shell[:int((segs_shell/n_tip)/2)+1]: # calculate point in the first half of the region between the first and second 'star tips'
        a_now = start_angle+(tau*t_now) # increase polar angle for each point
        angular_swerve = -((swerve*tau*sin(t_now*n_tip*tau+(tau/2))))*(((1/(1+exp(x_1-z_fraction*x_2)))*(1/(1+exp(x_1-(1-z_fraction)*x_2))))-(0.5*(sin(z_fraction*0.5*tau))**20)) # modify the polar angle of the current point to achieve a swerving shape in an opposing symmetric clockwise/anti-clockwise manner to make bulges appear to grow wider
        star_shape_wave = (tip_len*(0.5+0.5*(cos(t_now*n_tip*tau)))**2.5) # radial modifier for the current point due to the start-tip shape
        primary_z_wave = (bulge1*(sin(z_fraction*0.5*tau))**1) # radial modifier for the current point due to the main bulge
        secondary_z_waves = (((bulge2*(0.5+0.5*(cos((z_fraction+0.15)*2.3*tau)))**1.5))) # radial modifier for the current point due to the secondary bulges
        zigzag_wave = ((0.5-(0.5*cos(t_now*(segs_shell/2)*2*pi)))*(zag_min+(zag_max*(0.5+0.5*(cos(t_now*n_tip*tau)))**2))) if Output != 'Simple Plot' else 0 # radial modifier for the current point due to the zig-zag pattern around the circumference
        tiny_z_ripples = (rip_depth*(sin(z_fraction*rip_freq*tau))**2) if Output != 'Simple Plot' else 0 # radial modifier for the current point due to the tiny waves in the z direction
        r_now = r_0 + star_shape_wave + primary_z_wave + secondary_z_waves + zigzag_wave + tiny_z_ripples
        shell_steps.append(fc.polar_to_point(centre_now, r_now, a_now+angular_swerve)) # add the point to the current list of points based on the current angle and radius
    shell_steps.extend(fclab.reflectXYpolar_list(shell_steps, centre_now, start_angle+pi/n_tip)) # create the second half of the region between the first and second 'star tips' to achieve a rotationally repeating unit cell
    shell_steps = fc.move_polar(shell_steps, centre_now, 0, tau/n_tip, copy=True, copy_quantity=n_tip) # repeat the unit cell for all 'start tips'
    # previous_layer_point = shell_steps[-1]
    # if layer >0: print(f'approximate overhang for layer {layer}: {(360/tau)*fclab.angleZ(steps[-1], previous_layer_point)} degrees (exluding overhang due to mini z ripples)')
    steps.extend([fc.ExtrusionGeometry(width=EW, height=EH), fc.Printer(print_speed=print_speed)] + shell_steps) # set the current speed and extrusion geometry and add all the points for the shell for this layer
    if (target == 'gcode' and layer % layer_ratio == layer_ratio-1 and layer < frame_layers) or (target == 'visualize' and layer == 0 and frame_height > 0): # only print every few layers for gcode or the first layer for visualizing
        for t_now in t_steps_frame_line: # generate a wavey line in the Y direction - this assumes "start_angle = 0.75*tau"
            x_now = centre_xy+(frame_line_spacing_ratio*(frame_width_factor*EW))+(amp_1*t_now)*((0.5-0.5*cos((t_now**0.66)*3*tau))**1)
            y_now = centre_xy - frame_rad_inner - ((frame_rad_max-frame_rad_inner)*(1-t_now))
            wave_steps.append(fc.Point(x=x_now, y=y_now, z=z_now))
        wave_steps.extend(fc.arcXY(centre_now, frame_rad_inner, start_angle, pi/n_tip, int(64/n_tip))) # add points for half of the arc between the first and second 'star tips'
        wave_steps.extend(fclab.reflectXYpolar_list(wave_steps, centre_now, start_angle+pi/n_tip)) # reflect the arc and wavey line to complete one rotationally repreating unit cell
        wave_steps = fc.move_polar(wave_steps, centre_now, 0, tau/n_tip, copy=True, copy_quantity=n_tip) # repeat the unit cell for each 'star tip'
        steps.append(fc.ExtrusionGeometry(width=EW*frame_width_factor, height=EH*layer_ratio))
        steps.append(fc.Printer(print_speed=print_speed/(frame_width_factor*layer_ratio)))
        steps.extend(wave_steps)

# add annotations
if Output == 'Simple Plot': steps.append(fc.PlotAnnotation(point=fc.Point(x=centre_xy, y=50, z=0), label='Not all layers previewed - nor ripple texture'))
if Output == 'Detailed Plot': steps.append(fc.PlotAnnotation(point=fc.Point(x=centre_xy, y=50, z=0), label='Not all layers previewed'))
steps.append(fc.PlotAnnotation(point=fc.Point(x=centre_xy, y=25, z=0), label=f'Speed increases from {initial_print_speed} to {main_print_speed} mm/min during first {speedchange_layers} layers'))
steps.append(fc.PlotAnnotation(point=fc.Point(x=centre_xy, y=0, z=0), label=f'Avoid larger overhangs than default design - ripple texture exacerbates overhangs'))
steps.append(fc.PlotAnnotation(point=fc.Point(x=centre_xy, y=centre_xy, z=height+10), label=f'Try doubling speed - you may need to increase nozzle temperature'))

# transform design into plot or gcode
gcode_controls = fc.GcodeControls(printer_name=Printer_name, save_as = Design_name, initialization_data={'primer': 'front_lines_then_y', 'print_speed': initial_print_speed, 'nozzle_temp': Nozzle_temp, 'bed_temp': Bed_temp, 'fan_percent': Fan_percent, 'material_flow_percent': Material_flow_percent, 'print_speed_percent':Print_speed_percent, 'extrusion_width': EW, 'extrusion_height': EH})
plot_controls = fc.PlotControls(style='line', zoom=0.6, initialization_data={'extrusion_width': EW, 'extrusion_height': EH})
plot_controls.hide_annotations = False if Annotations else True
if target == 'gcode':
    gcode = fc.transform(steps, 'gcode', gcode_controls)
    open(f'{Design_name}.gcode', 'w').write(gcode)
    files.download(f'{Design_name}.gcode')
else:
    fc.transform(steps, 'plot', plot_controls)

# @markdown ##### **Details about the model parameters are given in code comments - many other parameters can also be edited in the code** *(double click this area to hide/show code)*