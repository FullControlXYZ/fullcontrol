#!/usr/bin/env python
# coding: utf-8

# ## notebooks
#  
# the following tutorials introduce the concept of FullControl, walk through its capabilities, and give tips for creating designs in FullControl
# 
# they refer to ***designs***, ***state***, ***things*** and ***results***  which are defined in the broad overview tutorial notebook
# 
# links will work in vscode, jupyter lab, etc. - the notebooks can also be accessed [online](https://github.com/FullControlXYZ/fullcontrol/tree/master/tutorials) and run in google colab
# 
# #### introductory documentation:
# 1. one-minute introduction to FullControl - [fast_demo.ipynb](fast_demo.ipynb)
# 1. broad overview of FullControl - [overview.ipynb](overview.ipynb)
# 
# #### technical use of FullControl:
# 1. create a ***design*** in FullControl with built-in objects - [state_objects.ipynb](state_objects.ipynb)
# 1. format gcode - [gcode_controls.ipynb](gcode_controls.ipynb)
#     - controls that can be used to adjust how a FullControl ***design*** is transsformed into a 'gcode' ***result***
# 1. format plots - [plot_controls.ipynb](plot_controls.ipynb)
#     - controls that can be used to adjust how a FullControl ***design*** is transformed into a 'plot' ***result***
# 1. geometric modeling functions - [geometry_functions.ipynb](geometry_functions.ipynb)
#     - demonstration of built-in geometry functions that can be used to create, modify or measure points (or lists of points)
# 1. other FullControl functions - [other_functions.ipynb](other_functions.ipynb)
# 
# #### tips and examples:
# 1. design tips - [design_tips.ipynb](design_tips.ipynb)
# 1. example model (nonplanar spacer) - [nonplanar_spacer.ipynb](../models/nonplanar_spacer.ipynb)
# 1. example model (nuts and bolts) - [nuts_and_bolts.ipynb](../models/nuts_and_bolts.ipynb)
# 1. design template - [design_template.ipynb](../models/design_template.ipynb)
# 1. design template for use in colab - [design_template_colab.ipynb](https://colab.research.google.com/github/FullControlXYZ/fullcontrol/blob/master/models/colab/design_template_colab.ipynb)
# 1. more designs are available on the fullcontrol [gists page](https://gist.github.com/fullcontrol-xyz)
# 
# #### FullControl lab:
# 1. FullControl lab geometry - [lab_geometry.ipynb](lab_geometry.ipynb)
# 1. four-axis example - [lab_four_axis_demo.ipynb](lab_four_axis_demo.ipynb)
# 1. five-axis example - [lab_five_axis_demo.ipynb](lab_five_axis_demo.ipynb)
# 1. stl output - [lab_stl_output.ipynb](lab_stl_output.ipynb)
#!/usr/bin/env python
# coding: utf-8

# # design tips
# 
# some anecdotal design considerations and examples / design-templates are provided here
# 
# <*this document is a jupyter notebook - if they're new to you, check out how they work:
# [link](https://www.google.com/search?q=ipynb+tutorial),
# [link](https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb),
# [link](https://colab.research.google.com/)*>
# 
# *run all cells in this notebook in order (keep pressing shift+enter)*

# In[ ]:


import fullcontrol as fc


# #### intellisense and auto-complete
# 
# FullControl objects and functions take advantage of intellisense and auto-complete
# - in jupyter lab, use tab and shift+tab for auto-complete and intellisense
#   - e.g. type 'fc.Poi' then tab then '(' then tab or shift+tab
# - in vscode, intellisense prompts pop-up automatically
# - check documentation for using intellisense in other software

# #### use the 'travel_to' function for convenience
# 
# the function fc.travel_to() is a convenient way to create a list of three steps: [Extruder(on=False), Point, Extruder(on=True)]

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0.2))
steps.append(fc.Point(x=5, y=5))
steps.extend([fc.Extruder(on=False), fc.Point(x=10, y=10), fc.Extruder(on=True)])
steps.append(fc.Point(x=15, y=15))
steps.extend(fc.travel_to(fc.Point(x=20, y=20)))
steps.append(fc.Point(x=25, y=25))
fc.transform(steps, 'plot')


# #### for-loops and fc.move()
# 
# layers are sometimes simple repetitions of the layer beneath, in which case, simply copying the layer's steps with fc.move() is useful (case 1 in the code below)
# 
# a for-loop can be used instead (case 2)
# 
# this allows other factors to be freely changed (case 3)

# In[ ]:


layers = 30

# case 1:
layer_steps = fc.rectangleXY(start_point=fc.Point(x=0,y=0,z=0.2), x_size=10, y_size=10)
steps = fc.move(layer_steps, fc.Vector(z=0.2), copy=True, copy_quantity=layers)
steps.insert(-2, fc.PlotAnnotation(label='case 1'))

# travel to start of case 2
steps.extend(fc.travel_to(fc.Point(x=20,y=0,z=0.2)))

# case 2:
for i in range(layers):
    steps.extend(fc.rectangleXY(start_point=fc.Point(x=20,y=0,z=i*0.2), x_size=10, y_size=10))
steps.insert(-2, fc.PlotAnnotation(label='case 2'))

steps.extend(fc.travel_to(fc.Point(x=40,y=0,z=0.2)))

# case 3: (x_size=10+i*0.2)
for i in range(layers):
    steps.extend(fc.rectangleXY(start_point=fc.Point(x=40,y=0,z=i*0.2), x_size=10+i*0.2, y_size=10))
steps.insert(-2, fc.PlotAnnotation(label='case 3'))

fc.transform(steps, 'plot')


# #### tau
# 
# tau equals 2*pi
# 
# tau represents a full circle in radians, whereas pi represents half a circle
# 
# the natural unit of measure is generally a full circle, not half a circle
# 
# if you want an arc that is 3/4 of a circle, arc length can be written as any of the following:
# 1. arc_length = 0.75 * tau
# 1. arc_length = 1.5 * pi
# 1. arc_length = 0.75 * 2 * pi
# 
# 0.75*tau is more natural and clearer
# 
# consider the equivalent for units of years (similar to tau) or half-years (similar to pi). which of the following statements is clearer (all equivalent to the above three statements)?
# 
# 1. I'm going on holiday in three quarters of a year
# 1. I'm going on holiday in one and a half half-years
# 1. I'm going on holiday in three quarters of two half-years
# 
# use tau!

# In[ ]:


from math import tau
centre = fc.Point(x=0, y=0, z=0.2)
steps = fc.arcXY(centre, 10, 0, 0.75*tau)
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence'))


# #### insert ***state***-changing instructions retrospectively
# 
# e.g. turn extrusion on/off after creating multiple copies of geometry

# In[ ]:


steps = [fc.Point(x=i, y=i, z=0.2) for i in range(10)]
steps.insert(4, fc.Extruder(on=False))
steps.insert(8, fc.Extruder(on=True))
fc.transform(steps,'plot')


# #### use fc.PlotAnnotions() and fc.GcodeComments() to debug and communicate designs
# 
# annotating the 3D plot is incredibly useful for communicating design intention or changes to state that aren't easy to show in a 3D geometric plot (e.g. fan speed)
# 
# python's [f-strings](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals) are a useful tool to generate annotation strings parametrically

# In[ ]:


steps = []
for i in range(13):
    steps.append(fc.Point(x=i+1, y=i+1, z=0))
    if i%2 == 0 and i<12:
        steps.append(fc.Fan(speed_percent=i*10))
        steps.append(fc.PlotAnnotation(label=f'fan speed {i*10}%'))
fc.transform(steps, 'plot', fc.PlotControls(style='line', color_type='print_sequence'))


# #### inspecting gcode
# 
# aside from opening the gcode file in a text editor or gcode-preview software, you can print a range of lines to screen, or use any of python's built-in functions to inspect the text

# In[ ]:


output_type = 2 # change this to be 1, 2, or 3

steps = [fc.Point(x=0,y=i,z=0) for i in range(11)]
gcode = fc.transform(steps, 'gcode')
gcode_list = (gcode.split('\n'))
if output_type == 1:
    print(gcode)
elif output_type == 2:
    print('\n'.join(gcode_list[5:8]))
elif output_type == 3:
    for gcode_line in (gcode_list):
        if 'G1 F' in gcode_line or 'G0 F' in gcode_line:
            print(gcode_line)


# #### concise point and relative-point definition
# 
# use P and R functions from the fullcontrol lab for concise definition of points in a design:
# - absolute points (P) -> *steps.append(****P****(x,y,z))*
# - relative points (R) -> *steps.append(****R****(x,y,z))*
# 
# fclab.setup_p() and fclab.setup_r() functions are used to create the P and R functions
# 
# the setup_r() function must be passed the variable you are using for your list of steps. relative points are always defined relative to the last point in that list

# In[ ]:


import lab.fullcontrol as fclab

steps = []
P = fclab.setup_p()
R = fclab.setup_r(steps)

steps.append(P(40, 40, 0))
steps.append(R(0, 1, 0))
steps.append(R(1, 0, 0))

for step in steps: print(step)


# #### new geometry functions
# 
# create your own geometry functions
# 
# if you create useful geometry functions, add them to FullControl so everyone can benefit (see contribution guidelines on [github](https://github.com/FullControlXYZ/fullcontrol))
# 
# also see the section later in this notebook about using AI to generate geometric functions

# In[ ]:


def saw_wave_x(start_point: fc.Point, length: float, amplitude: float, periods: int) -> list:
    period_length = length/periods
    steps_wave = []
    for i in range(periods):
        steps_wave.append(fc.Point(x=start_point.x+period_length*i, y=start_point.y, z=start_point.z))
        steps_wave.append(fc.Point(x=start_point.x+period_length*i, y=start_point.y+amplitude, z=start_point.z))
    steps_wave.append(fc.Point(x=start_point.x+length, y=start_point.y, z=start_point.z))   
    return steps_wave
                 
steps = []
steps.extend(saw_wave_x(fc.Point(x=20, y=20, z=0), 50, 10, 20))
steps.extend(saw_wave_x(steps[-1], 50, 20, 10))
steps.extend(saw_wave_x(steps[-1], 50, 10, 20))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence'))


# #### assemble ***design-blocks*** to create a ***design***

# In[ ]:


centre = fc.Point(x=0, y=0, z=0.2)
block1 = fc.spiralXY(centre, 0.5, 20, 0, 40, 2000)
block2 = fc.helixZ(centre, 20, 0, 0, 60, 0.3, 2200)
steps = block1 + block2
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence'))


# #### use fc.linspace() to create list of evenly-spaced numbers

# In[ ]:


print('e.g. "fc.linspace(0,1,5)": ' + str(fc.linspace(0,1,5)))
from math import tau
centre = fc.Point(x=0, y=0, z=0)
point_count = 100
radii = fc.linspace(10,20,point_count)
angles = fc.linspace(0,tau*2,point_count)
steps = [fc.polar_to_point(centre, radii[i], angles[i]) for i in range(point_count)]
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence'))


# #### polar_coordinates
# 
# points can be generated based on a polar-coordinates definition
# 
# state an origin, polar radius and polar angle
# 
# the first two points in the code below are identical but defined by different methods

# In[ ]:


origin = fc.Point(x=0, y=0, z=0)
from math import tau

point_cart = fc.Point(x=10,y=0,z=0)
print(point_cart)
point_polar1 = fc.polar_to_point(origin, 10, 0)
print(point_polar1)
point_polar2 = fc.polar_to_point(origin, 10, tau/8)
print(point_polar2)
point_polar3 = fc.polar_to_point(origin, 10, tau/4)
print(point_polar3)
point_polar4 = fc.polar_to_point(origin, 10, -tau/4)
print(point_polar4)


# #### vase mode
# 
# polar coordinates allow vase mode to be achieved easily

# In[ ]:


from math import cos, tau
layers = 50
segments_per_layer = 64
centre = fc.Point(x=50, y=50, z=0)
layer_height = 0.1
steps = []
for i in range(layers*segments_per_layer+1):
    # find useful measures of completion
    layer_fraction = (i%segments_per_layer)/segments_per_layer
    total_fraction = (int(i/segments_per_layer)+layer_fraction)/layers
    # calculate polar details
    angle = layer_fraction*tau
    radius = 5+1*cos(tau*(total_fraction))
    centre.z = layer_height*layers*total_fraction
    # add point
    steps.append(fc.polar_to_point(centre, radius, angle))
fc.transform(steps, 'plot', fc.PlotControls(zoom=0.8))


# #### parametric maths equations with 't' (cartesian)
# 
# use desmos to develop equations: [cartesian desmos link](https://www.desmos.com/calculator/2usosgsxtd)

# In[ ]:


from math import cos, tau
x_size = 20
y_offset, y_amplitude, waves = 5, 5, 3
t_steps = fc.linspace(0, 1, 101) # [0, 0.01, 0.02, ... , 0.99, 1]
steps = []
for t_now in t_steps:
    x_now = x_size*t_now
    y_now = y_offset+y_amplitude*cos(t_now*tau*waves)
    z_now = 0.2
    steps.append(fc.Point(x=x_now, y=y_now, z=z_now))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence'))


# #### parametric maths equations with 't' (polar)
# 
# use desmos to develop equations: [polar desmos link](https://www.desmos.com/calculator/nropwukta4)

# In[ ]:


from math import cos, tau
centre = fc.Point(x=0, y=0, z=0)
inner_rad, rad_fluctuation, waves = 4, 1, 12
t_steps = fc.linspace(0, 1, 1001)  # [0, 0.001, 0.002, ... , 0.999, 1]
steps = []
for t_now in t_steps:
    a_now = t_now*tau
    r_now = inner_rad+rad_fluctuation*cos(t_now*tau*waves)
    z_now = 0
    steps.append(fc.polar_to_point(centre, r_now, a_now))
steps = fc.move(steps,fc.Vector(z=0.1),copy=True, copy_quantity=10)
fc.transform(steps, 'plot')


# #### 'post-process' a ***design*** or ***design-block***
# 
# the following example creates a helical toolpath and then 'post-processes' it to change its geometry. the 'post-process' bit of code would work on different types of original geometry (e.g. a lattice-filled cylinder)

# In[ ]:


# create a basic simple geometry (a cylinder) that will be modified retrospectively
centre = fc.Point(x=50, y=50, z=0)
steps = fc.helixZ(centre, start_radius=10, end_radius=10, start_angle=0, n_turns=50, pitch_z=0.167, segments=50*64)
steps.append(fc.PlotAnnotation(point = fc.Point(x=50, y=50, z=10), label='original geometry'))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', zoom=0.7))

# 'post-process' the geometry to change it
z_max = 25
for step in steps:
    if isinstance(step, fc.Point):
        step.x -= 0.8*(step.x-centre.x)*(step.z/z_max)
        step.y -= 0.8*(step.y-centre.y)*(step.z/z_max)
        step.z -= (((step.y-centre.y)/2.5)**2)*(step.z/z_max)
steps[-1] = fc.PlotAnnotation(point = fc.Point(x=50, y=50, z=10), label="'postprocessed' geometry")
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', zoom=0.7))


# the following code cell shows a slightly more complex 'post-process', where a linear wave is created and then 'wrapped' around a cylinder to form an arc
# 
# this may be useful if it's easier to define some particular geometry in a linear format than in a curved format

# In[ ]:


from math import tau
rad, rad_fluc, segs_per_period = 20, 5, 12
periods = 25
period_length = 3  # calculated to make sure the wave is the length of the circle circumference
steps = fc.sinewaveXYpolar(fc.Point(x=rad, y=0, z=0.2), 0.75*tau, rad_fluc, period_length, periods, segs_per_period)
steps.append(fc.PlotAnnotation(point=fc.Point(x=1.5*rad, y=-60, z=10), label='original geometry'))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence'))

def linear_to_arc(steps: list, centre: fc.Point, radius: float) -> list:
    '''this function assumes the linear geometry (list of points: 'steps') is oriented in 
    the y direction and positioned in the positive x-direction from the centre point. it 
    is 'wrapped' around an arc/circle dictated by radius. it is possible to wrap multiple 
    times. return list of translated points
    '''
    steps_wrapped = []
    for step in steps:
        rad_step = step.x - centre.x
        angle_step = (step.y - centre.y) / radius
        steps_wrapped.append(fc.polar_to_point(centre, rad_step, angle_step))
    return steps_wrapped

del steps[-1] # remove the PlotAnnotation
steps_wrapped = linear_to_arc(steps, fc.Point(x=0, y=0, z=0.2), 15)
steps_wrapped.append(fc.PlotAnnotation(point=fc.Point(x=0, y=0, z=10), label="'post-processed' geometry"))

fc.transform(steps_wrapped, 'plot', fc.PlotControls(color_type='print_sequence'))


# #### generation speed
# 
# don't worry too much about speed - future enhancements to the FullControl source code can easily:
# 
# - increase speed all-round
# - allow quick previews
# - include lightweight variants of objects with less functionality but greater speed
# - explain how to generate designs quickly for specific ***results*** - e.g. no 'plot' option for fc.transform(), but greater gcode-generation speed
# - explain how to create custom versions of FullControl for specific applications that only include strictly necessary functionality
# 
# immediate opportunities to increase the speed of plot previews:
# 
# - use ***design-blocks*** (described above) - create and preview them one at a time
# - reducing segments for the 'plot' result but not the 'gcode' result
# - increasing layer height to be unrealistically high for the 'plot' result but not the 'gcode' result
# - create your design such that frequently changed ***state***-changing objects that don't affect the plot are not created when creating a ***design*** (see the code-block below)
#     
# - for ***designs*** with lots of travel, create your design such that travel controls (fc.Extruder(on=###)) do not execute when creating a ***design*** for a 'plot' ***result***
#     - this means plotly plots the whole design as a single line series (fast), as opposed to lots of individual line series (slow)
# 

# In[ ]:


result_type = 'plot'  # set as 'gcode' or 'plot'
steps = []
for i in range(6):
    if result_type != 'plot':
        # fan speed does not affect the 'plot' result so doesn't need to be added to the design result_type == 'plot'
        steps.append(fc.Fan(speed_percent=100*i/5))
    steps.append(fc.Point(x=5*(i+1), y=5*((i+1)%2), z=0.2))
print(f"the design specifically for the '{result_type}' result contains {len(steps)} steps:")
for step in steps: print(type(step).__name__)
fc.transform(steps, result_type, fc.PlotControls(color_type='print_sequence'))


# #### use AI to create designs or geometry functions
# 
# this is most suitable for users who have already got a good understanding of how to use FullControl since there is a reasonable risk that AI-generated code will not exactly match FullControl's requirements (e.g. it may generate a numpy array, or a dict instead of a list of FullControl Point objects)
# 
# example [chatGPT](https://chat.openai.com/) request:
# ```
# In python, a pydantic BaseModel class for a point has been imported in a module named fc
# 
# Create a list of points for a spiral with defined start radius, end radius, turns, number of points and centre point
# ```
# 
# the chatGPT output is given below. it is very sensitive to the question and can generate different responses when asked the same question twice. for the result generated below, chatGPT assumed the Point class was imported from the fc module rather than importing the whole fc module as done in these tutorial notebooks. therefore it doesn't use the fc.Point terminology, it just uses Point. a reasonable level of python knowledge is required to ensure the output can be tweaked as needed to work with FullControl as well as a good understanding of FullControl. E.g. this chatGPT code has no z values, but at least one point in your design must have a z value to allow a 3D plot
# 
# chatGPT output:
# 
# ```
# from math import cos, sin, pi
# from fc import Point
# from typing import List
# 
# def generate_spiral_points(start_radius: float, end_radius: float, turns: int, num_points: int, center: Point) -> List[Point]:
#     points = []
#     radius_diff = end_radius - start_radius
#     angle_step = 2 * pi * turns / num_points
#     for i in range(num_points):
#         radius = start_radius + radius_diff * i / (num_points - 1)
#         angle = i * angle_step
#         x = center.x + radius * cos(angle)
#         y = center.y + radius * sin(angle)
#         points.append(Point(x=x, y=y))
#     return points
# ```
# 

# In[ ]:


from math import cos, sin, pi

def generate_spiral_points(start_radius: float, end_radius: float, turns: int, num_points: int, center: fc.Point) -> list:
    points = []
    radius_diff = end_radius - start_radius
    angle_step = 2 * pi * turns / num_points
    for i in range(num_points):
        radius = start_radius + radius_diff * i / (num_points - 1)
        angle = i * angle_step
        x = center.x + radius * cos(angle)
        y = center.y + radius * sin(angle)
        points.append(fc.Point(x=x, y=y, z=center.z)) # added 'fc.' and a z value is required for FullControl to create a plot in 3D space
    return points

steps = generate_spiral_points(10, 20, 4, 128, fc.Point(x=50, y=50, z=0))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence'))

#!/usr/bin/env python
# coding: utf-8

# # FullControl 1-minute demo
# 
# #### run all cells in this notebook in order (keep pressing shift+enter)
# 
# this quick demo shows how a design can be created with a list of points for nozzle movement with or without extrusion
# 
# the design is visually previewed, then gcode is created for a specific printer and saved to a file
# 
# for more information, see the [FullControl overview notebook](overview.ipynb)
# 
# <*this document is a jupyter notebook - if they're new to you, check out how they work:
# [link](https://www.google.com/search?q=ipynb+tutorial),
# [link](https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb),
# [link](https://colab.research.google.com/)*>
# 
# *run all cells in this notebook in order (keep pressing shift+enter)*
# 
# #### first, import fullcontrol to have access to its capabilities

# In[ ]:


import fullcontrol as fc


# #### create and preview a design (a list of steps telling the printer what to do)

# In[ ]:


# create an empty list called steps
steps=[]
# add points to the list
steps.append(fc.Point(x=40,y=40,z=0.2))
steps.append(fc.Point(x=50,y=50))
steps.append(fc.Point(x=60,y=40))
# turn the extruder on or off
steps.append(fc.Extruder(on=False))
steps.append(fc.Point(x=40,y=40,z=0.4))
steps.append(fc.Extruder(on=True))
steps.append(fc.Point(x=50,y=50))
steps.append(fc.Point(x=60,y=40))
# transform the design into a plot
fc.transform(steps, 'plot')


# #### set filename, printer and print settings

# In[ ]:


filename = 'my_design'
printer = 'ender_3' 
# printer options: generic, ultimaker2plus, prusa_i3, ender_3, cr_10, bambulab_x1, toolchanger_T0, toolchanger_T1, toolchanger_T2, toolchanger_T3
print_settings = {'extrusion_width': 0.5,'extrusion_height': 0.2, 'nozzle_temp': 210, 'bed_temp': 40, 'fan_percent': 100}
# 'extrusion_width' and 'extrusion_height' are the width and height of the printed line)


# #### save gcode file to the same directory as this notebook
# 
# do not edit this line of code - it uses values defined in the previous code cells
# 
# make sure you execute the previous cells before running this one

# In[ ]:


fc.transform(steps, 'gcode', fc.GcodeControls(printer_name=printer, save_as=filename, initialization_data=print_settings))


# #### get creative!
# 
# check out [other tutorials](contents.ipynb) to see how to create designs like this gear/thread example with just one line of code

# In[ ]:


steps = [fc.polar_to_point(centre=fc.Point(x=0, y=0, z=i*0.005), radius=10, angle=i*4.321) for i in range(1000)]
fc.transform(steps, 'plot', fc.PlotControls(neat_for_publishing=True, zoom=0.7))


# #### random mesh example

# In[ ]:


from math import tau
from random import random
steps=[fc.polar_to_point(centre=fc.Point(x=0, y=0, z=i*0.001), radius=10+5*random(), angle=i*tau/13.8) for i in range(4000)]
fc.transform(steps, 'plot', fc.PlotControls(neat_for_publishing=True, zoom=0.7))

#!/usr/bin/env python
# coding: utf-8

# # GcodeControls adjust how a ***design*** is transformed into a 'gcode' ***result***
# 
# ***designs*** are transformed into 'gcode' according to some default settings which can be overwritten with a GcodeControls object with the following attributes (all demonstrated in this notebook):
# 
# - `save_as` - used to save the gcode directly to a .gcode file
# - `include_date` - append filename with date+time (default: True)
# - `printer_name` - used to choose which printer the gcode should be formatted for
#     - a selection of printers are built in, which is expected to be extended. documentation for adding new printers will be provided in the future
# - `initialization_data` - used to change the initial print conditions/settings that are established before the steps in the ***design*** are evaluated
# 
# <*this document is a jupyter notebook - if they're new to you, check out how they work:
# [link](https://www.google.com/search?q=ipynb+tutorial),
# [link](https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb),
# [link](https://colab.research.google.com/)*>
# 
# *run all cells in this notebook in order (keep pressing shift+enter)*

# In[ ]:


import fullcontrol as fc


# ## save to file
# 
# use the `save_as` attribute of a GcodeControls object to save the gcode to a file in the same directory as this notebook, with the filename appended by date and time
# 
# set `include_date` = False to remove date and time

# In[ ]:


steps = []
steps.append(fc.Point(x=30, y=30, z=0.2))
steps.append(fc.Point(x=60))
# option 1 (use built-in function):
gcode_controls = fc.GcodeControls(save_as='my_design') # filename includes date+time
fc.transform(steps, 'gcode', gcode_controls)
gcode_controls = fc.GcodeControls(save_as='my_design', include_date = False) # filename doesn't include date+time
fc.transform(steps, 'gcode', gcode_controls)
# option 2 (save gcode string to file manually):
gcode = fc.transform(steps, 'gcode')
open('my_file.gcode', 'w').write(gcode)


# ## choose printer
# 
# change which printer to output gcode for with the 'printer_name' attribute
# 
# current options:
# 
# - 'generic' *(default)*
# - 'ultimaker2plus'
# - 'prusa_i3'
# - 'ender_3'
# - 'cr_10'
# - 'bambulab_x1'
# - 'toolchanger_T0'
# - 'toolchanger_T1'
# - 'toolchanger_T2'
# - 'toolchanger_T3'
# - 'custom'
# 
# the option 'generic' is default and outputs gcode with no start/end gcode except for the command M83, since omitting this command is a common source of error
# 
# the option 'custom' doesn't generate any start_gcode at all and allows custom starting procedures to be created as demonstrated later in this notebook

# In[ ]:


steps = []
steps.append(fc.Point(x=30, y=30, z=0.2))
steps.append(fc.Point(x=60))
gcode_controls = fc.GcodeControls(printer_name='toolchanger_T0', save_as='my_design')
fc.transform(steps, 'gcode', gcode_controls)


# ## change initial settings
# 
# the 'initialization_data' attribute is used to pass a python 'dictionary' capturing information about printing conditions/settings at the start of the printing process
# 
# currently, the dictionary can contain any of the aspects listed below
# 
# a description or the object type ([defined in state objects notebook](state_objects.ipynb)) is displayed next to each term along with default values - individual printers may over-ride these default values or they can be manually over-ridden by including them in the dictionary that is passed to the fc.transform() function when it generates gcode
# 
# - 'print_speed': 1000 - Printer(print_speed)
# - 'travel_speed': 8000 - Printer(travel_speed)
# - 'area_model': 'rectangle' - ExtrusionGeometry(area_model)
# - 'extrusion_width': 0.4 - ExtrusionGeometry(width)
# - 'extrusion_height': 0.2 - ExtrusionGeometry(height)
# - 'nozzle_temp': 210 - Hotend(temp)
# - 'bed_temp': 40 - Buildplate(temp)
# - 'fan_percent': 100 - Fan(speed_percent)
# - 'print_speed_percent': 100 - used in start_gcode for an M220 command
# - 'material_flow_percent': 100 - used in start_gcode for an M221 command
# - 'e_units': 'mm' - Extruder(units)
# - 'relative_e': True - Extruder(relative_gcode)
# - 'dia_feed': 1.75 - Extruder(dia_feed)
# - 'primer': 'front_lines_then_y' - see later section about built-in primer options

# #### default settings

# In[ ]:


steps = [fc.Point(x=30, y=30, z=0.2), fc.Point(x=60)]
print(fc.transform(steps, 'gcode'))


# #### initial speed and fan
# 
# as described above, the default printer is called 'generic' and outputs gcode with no start/end gcode except for the command M83. however, overriding an initial setting results in the appropriate gcode being added to start_gcode

# In[ ]:


steps = [fc.Point(x=30, y=30, z=0.2), fc.Point(x=60)]
initial_settings = {
    "print_speed": 2000,
    "travel_speed": 4000,
    "nozzle_temp": 280,
    "bed_temp": 80,
    "fan_percent": 40,
}
gcode_controls = fc.GcodeControls(initialization_data=initial_settings)
print(fc.transform(steps, 'gcode', gcode_controls))


# #### extrusion width and parameters that affect E in gcode

# In[ ]:


steps = [fc.Point(x=30, y=30, z=0.2), fc.Point(x=60)]
initial_settings = {
    "extrusion_width": 0.8,
    "extrusion_height": 0.3,
    "e_units": "mm3",
    "relative_e": False,
    "dia_feed": 2.85,
}
gcode_controls = fc.GcodeControls(initialization_data=initial_settings)
print(fc.transform(steps, 'gcode', gcode_controls))


# #### setting flow % and speed %
# 
# these aspects change the over-ride values for speed % (gcode M220) and flow % (gcode M221). They don't change the values written for F terms and E terms in gcode. The printer display screen should show these values correctly during printing and allow them to be changed after the print has started

# In[ ]:


steps = [fc.Point(x=30, y=30, z=0.2), fc.Point(x=60)]
initial_settings = {
    "print_speed_percent": 100,
    "material_flow_percent": 100,
}
gcode_controls = fc.GcodeControls(initialization_data=initial_settings)
print(fc.transform(steps, 'gcode', gcode_controls))


# #### primer
# 
# some basic options to add a primer before your design begins printing are included in this release of FullControl. a good alternative to using a built-in primer, is to manually design a primer at the beginning of the list of steps in a ***design***. such a primer can be truly optimized for the individual design to ensure printing begins perfectly and to minimize the risk of first-layer defects. see an example of this below
# 
# current options for primers are:
# 
# - 'front_lines_then_x' - this involves printing some lines on the front of the bed before moving in the **x** direction to the start point of the ***design***
# - 'front_lines_then_y' - similar to above except move in **y** direction
# - 'front_lines_then_xy' - similar to above except move in diagonal **xy** direction
# - 'x' - move from the position at the end of start_gcode to the start point of the ***design*** along the **x** direction (after a y-direction move)
# - 'y' - similar to above except move in x first, then y to the start point
# - 'xy' - print directly from the end of the start gcode to the start point
# - 'travel' - travel from the end of the start gcode to the start point
# 

# In[ ]:


steps = [fc.Point(x=30, y=30, z=0.2), fc.Point(x=60)]
gcode_controls = fc.GcodeControls(initialization_data={"primer": "front_lines_then_xy"})
print(fc.transform(steps, 'gcode', gcode_controls))


# #### custom primer
# 
# an easy way to add a custom primer, is to include it at the beginning of the ***design***
# 
# set the gcode initialization data to have the 'travel' primer-type to quickly travel to the start point of the custom primer
# 
# the ***design*** in the following code cell is transformed to a 'plot' ***result*** rather than 'gcode' for ease of inspection

# In[ ]:


design_steps = [fc.polar_to_point(centre=fc.Point(x=0, y=0, z=i*0.005), radius=10+10*(i%2), angle=i) for i in range(500)]
primer_steps = fc.spiralXY(fc.Point(x=0, y=0, z=0.2), 2, 8, 0, 4, 128)
steps = primer_steps + design_steps
steps.append(fc.PlotAnnotation(point=fc.Point(x=2, y=0, z=0.2), label='primer start'))
steps.append(fc.PlotAnnotation(point=fc.Point(x=10, y=0, z=0.1), label='design start'))
steps.append(fc.PlotAnnotation(point=fc.Point(x=0, y=0, z=10), label='internal spiral-primer ends near the main-design start point'))
fc.transform(steps, 'plot')


# ## custom printer template
# 
# add your own printer by updating the code in the following code cell, which uses the 'custom' printer-type and includes appropriate FullControl objects as the first few steps in the ***design***
# 
# the following commands generate gcode during initialization of the printer in FullControl, and therefore, it's advisable **not** to use them to avoid their associated gcode appearing before your starting procedure:
# - relative_e / nozzle_temp / bed_temp / fan_percent / print_speed_percent / material_flow_percent / primer
# 
# instead, these aspects should be controlled by the custom starting procedure at the start of your ***design***, including turning the extruder on at the appropriate time
# 
# *future documentation will explain how to add you own printer to the library of printers in the python source code*

# In[ ]:


# create the initialize procedure (i.e. start_gcode)
initial_settings = {
    "extrusion_width": 0.8,
    "extrusion_height": 0.3,
    "e_units": "mm3",
    "dia_feed": 2.85,
    "primer": "no_primer",
    "print_speed": 2000,
    "travel_speed": 4000
}
gcode_controls = fc.GcodeControls(printer_name='custom', initialization_data=initial_settings)
starting_procedure_steps = []
starting_procedure_steps.append(fc.ManualGcode(text='\n; #####\n; ##### beginning of start procedure\n; #####'))
starting_procedure_steps.append(fc.ManualGcode(text='G28 ; home'))
starting_procedure_steps.append(fc.GcodeComment(text='heat bed 10 degrees too hot'))
starting_procedure_steps.append(fc.Buildplate(temp=60, wait=True))
starting_procedure_steps.append(fc.GcodeComment(text='allow bed to cool to the correct temp and heat up nozzle'))
starting_procedure_steps.append(fc.Hotend(temp=220, wait=False))
starting_procedure_steps.append(fc.Buildplate(temp=50, wait=True))
starting_procedure_steps.append(fc.Hotend(temp=220, wait=True))
starting_procedure_steps.append(fc.Fan(speed_percent=100))
starting_procedure_steps.append(fc.Extruder(relative_gcode=True))
starting_procedure_steps.append(fc.Point(x=10, y=10, z=0.4))
starting_procedure_steps.append(fc.ManualGcode(text='; #####\n; ##### end of start procedure\n; #####\n'))

# create the design
design_steps = []
design_steps.append(fc.Point(x=0, y=0, z=0.2))
design_steps.append(fc.Extruder(on=True))
design_steps.append(fc.Point(x=10, y=0, z=0.2))

# combine start procedure and design to create the overall procedure
steps = starting_procedure_steps + design_steps
print(fc.transform(steps, 'gcode', gcode_controls))

#!/usr/bin/env python
# coding: utf-8

# # geometry functions allow a ***design*** to be created more easily
# 
# the geometry functions here allow points to be created (part I), measured (part II) and moved/copied (part III)
# 
# geometry functions work best when x, y and z are all defined for all points
# 
# 'tau' (equal to 2*pi) is used throughout this notebook - see tau section of the [design tips notebook](design_tips.ipynb) for further details
# 
# <*this document is a jupyter notebook - if they're new to you, check out how they work:
# [link](https://www.google.com/search?q=ipynb+tutorial),
# [link](https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb),
# [link](https://colab.research.google.com/)*>
# 
# *run all cells in this notebook in order (keep pressing shift+enter)*

# In[ ]:


import fullcontrol as fc
from math import tau, sin


# ## I. create points
# 
# single points:
# - points defined by polar coordinates
# - midpoint of two points
# 
# lists of points:
# - arc
# - arc with variable radius
# - elliptical arc
# - rectangle
# - circle
# - polygon
# - spiral
# - helix (optionally with variable radius)
# - squarewave
# - segmented line

# #### midpoint() and polar_to_point() (point defined by polar coordinates)

# In[ ]:


pt1 = fc.Point(x=0,y=0,z=0)
pt2 = fc.Point(x=0,y=10,z=0)
pt3 = fc.polar_to_point(pt2, 10, tau/8)
pt4 = fc.midpoint(pt1, pt2)
steps = [pt1, pt2, pt3, pt4]
steps.append(fc.PlotAnnotation(point=pt4, label="midpoint between point 1 and point 2"))
steps.append(fc.PlotAnnotation(point=pt1, label="point 1"))
steps.append(fc.PlotAnnotation(point=pt2, label="point 2"))
steps.append(fc.PlotAnnotation(point=pt3, label="point defined by polar coordinates relative to point 2"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))


# #### rectangle

# In[ ]:


start_point = fc.Point(x=10, y=10, z=0)
x_size = 10
y_size = 5
clockwise = True
steps = fc.rectangleXY(start_point, x_size, y_size, clockwise)
steps.append(fc.PlotAnnotation(point=steps[-1], label="start/end"))
steps.append(fc.PlotAnnotation(point=steps[1], label="first point after start"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))


# #### circle

# In[ ]:


centre_point = fc.Point(x=10, y=10, z=0)
radius = 10
start_angle = 0
segments = 32
clockwise = True
steps = fc.circleXY(centre_point, radius, start_angle, segments, clockwise)
steps.append(fc.PlotAnnotation(point=steps[-1], label="start/end"))
steps.append(fc.PlotAnnotation(point=steps[1], label="first point after start"))
steps.append(fc.PlotAnnotation(point=centre_point, label="centre"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))


# #### ellipse

# In[ ]:


centre_point = fc.Point(x=10, y=10, z=0)
a = 10
b = 5
start_angle = 0
segments = 32
clockwise = True
steps = fc.ellipseXY(centre_point, a, b, start_angle, segments, clockwise)
steps.append(fc.PlotAnnotation(point=steps[-1], label="start/end"))
steps.append(fc.PlotAnnotation(point=steps[1], label="first point after start"))
steps.append(fc.PlotAnnotation(point=centre_point, label="centre"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))


# #### polygon

# In[ ]:


centre_point = fc.Point(x=10, y=10, z=0)
enclosing_radius = 10
start_angle = 0
sides = 6
clockwise = True
steps = fc.polygonXY(centre_point, enclosing_radius, start_angle, sides, clockwise)
steps.append(fc.PlotAnnotation(point=steps[-1], label="start/end"))
steps.append(fc.PlotAnnotation(point=steps[1], label="first point after start"))
steps.append(fc.PlotAnnotation(point=centre_point, label="centre"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))


# #### arc

# In[ ]:


centre_point = fc.Point(x=10, y=10, z=0)
radius = 10
start_angle = 0
arc_angle = 0.75*tau
segments = 64
steps = fc.arcXY(centre_point, radius, start_angle, arc_angle, segments)
steps.append(fc.PlotAnnotation(point=steps[-1], label="end"))
steps.append(fc.PlotAnnotation(point=steps[0], label="start"))
steps.append(fc.PlotAnnotation(point=centre_point, label="centre"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))


# #### variable arc

# In[ ]:


centre_point = fc.Point(x=10, y=10, z=0)
radius = 10
start_angle = 0
arc_angle = 0.75*tau
segments = 64
radius_change = -6
z_change = 0
steps = fc.variable_arcXY(centre_point, radius, start_angle, arc_angle, segments, radius_change, z_change)
steps.append(fc.PlotAnnotation(point=steps[-1], label="end"))
steps.append(fc.PlotAnnotation(point=steps[0], label="start"))
steps.append(fc.PlotAnnotation(point=centre_point, label="centre"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))


# #### elliptical arc

# In[ ]:


centre_point = fc.Point(x=10, y=10, z=0)
a = 10
b = 5
start_angle = 0
arc_angle = 0.75*tau
segments = 64
steps = fc.elliptical_arcXY(centre_point, a, b, start_angle, arc_angle, segments)
steps.append(fc.PlotAnnotation(point=steps[-1], label="end"))
steps.append(fc.PlotAnnotation(point=steps[0], label="start"))
steps.append(fc.PlotAnnotation(point=centre_point, label="centre"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))


# #### spiral

# In[ ]:


centre_point = fc.Point(x=10, y=10, z=0)
start_radius = 10
end_radius = 8
start_angle = 0
n_turns = 5
segments = 320
z_change = 0
clockwise = True
steps = fc.spiralXY(centre_point, start_radius, end_radius, start_angle, n_turns, segments, clockwise)
steps.append(fc.PlotAnnotation(point=steps[-1], label="end"))
steps.append(fc.PlotAnnotation(point=steps[0], label="start"))
steps.append(fc.PlotAnnotation(point=centre_point, label="centre"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))

# spirals are also possible by using fc.variable_arcXY with 'arc_angle' set to the number of passes * tau and 'radius_change' set to the total change in radius over the whole spiral


# #### helix

# In[ ]:


centre_point = fc.Point(x=10, y=10, z=0)
start_radius = 10
end_radius = 10
start_angle = 0
n_turns = 5
pitch_z = 0.4
segments = 320
clockwise = True
steps = fc.helixZ(centre_point, start_radius, end_radius, start_angle, n_turns, pitch_z, segments, clockwise)
steps.append(fc.PlotAnnotation(point=steps[-1], label="end"))
steps.append(fc.PlotAnnotation(point=steps[0], label="start"))
steps.append(fc.PlotAnnotation(point=centre_point, label="centre"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))

# helices are also possible by using fc.variable_arcXY with 'arc_angle' set to the number of passes * tau and 'z_change' set to the total helix length


# #### waves

# In[ ]:


# wave 1
start_point = fc.Point(x=10, y=10, z=0)
direction = fc.Vector(x=1,y=0)
amplitude = 5
line_spacing = 1
periods = 10
extra_half_period = False
extra_end_line = False
steps = fc.squarewaveXY(start_point, direction, amplitude, line_spacing, periods, extra_half_period, extra_end_line)
steps.append(fc.PlotAnnotation(point=start_point, label="start of wave 1"))

# wave 2
start_point = fc.Point(x=10, y=20, z=0)
extra_half_period = True
# steps.extend([fc.Extruder(on=False), start_point, fc.Extruder(on=True)])
steps.extend(fc.travel_to(start_point))
steps.extend(fc.squarewaveXY(start_point, direction, amplitude, line_spacing, periods, extra_half_period, extra_end_line))
steps.append(fc.PlotAnnotation(point=start_point, label="start of wave 2"))
steps.append(fc.PlotAnnotation(label="extra half period"))

# wave 3
start_point = fc.Point(x=10, y=30, z=0)
extra_half_period = True
extra_end_line = True
# steps.extend([fc.Extruder(on=False), start_point, fc.Extruder(on=True)])
steps.extend(fc.travel_to(start_point))
steps.extend(fc.squarewaveXY(start_point, direction, amplitude, line_spacing, periods, extra_half_period, extra_end_line))
steps.append(fc.PlotAnnotation(point=start_point, label="start of wave 3"))
steps.append(fc.PlotAnnotation(label="extra end-line"))

# wave 4
start_point = fc.Point(x=10, y=40, z=0)
direction_polar = tau/8
# steps.extend([fc.Extruder(on=False), start_point, fc.Extruder(on=True)])
steps.extend(fc.travel_to(start_point))
steps.extend(fc.squarewaveXYpolar(start_point, direction_polar, amplitude, line_spacing, periods, extra_half_period, extra_end_line))
steps.append(fc.PlotAnnotation(point=start_point, label="start of wave 4 (squarewaveXYpolar)"))
steps.append(fc.PlotAnnotation(label="wave in polar direction tau/8"))

# wave 5
start_point = fc.Point(x=40, y=45, z=0)
direction_polar = 0.75*tau
tip_separation = 2
extra_half_period = False
# steps.extend([fc.Extruder(on=False), start_point, fc.Extruder(on=True)])
steps.extend(fc.travel_to(start_point))
steps.extend(fc.trianglewaveXYpolar(start_point, direction_polar, amplitude, tip_separation, periods, extra_half_period))
steps.append(fc.PlotAnnotation(point=start_point, label="start of wave 5 (trianglewaveXYpolar)"))

# wave 5
start_point = fc.Point(x=50, y=35, z=0)
direction_polar = 0.75*tau
period_lenth = 2
segments_per_period = 16
extra_half_period = False
phase_shift = 0
# steps.extend([fc.Extruder(on=False), start_point, fc.Extruder(on=True)])
steps.extend(fc.travel_to(start_point))
steps.extend(fc.sinewaveXYpolar(start_point, direction_polar, amplitude, period_lenth, periods, segments_per_period, extra_half_period, phase_shift))
steps.append(fc.PlotAnnotation(point=start_point, label="start of wave 6 (sinewaveXYpolar)"))

fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))


# #### segmented line
# 
# typically, a straight line is created with only start and end points. this means the shape of the line cannot be edited after creation. it is sometimes advantageous to be able to change the shape retrospectively. if the line is defined as a series of segments, all the points along the line can be edited after creation. the example below shows a straight line being modified based on each point
# 
# the function segmented_line() allows a segmented line to be created easily based on a start point and end point

# In[ ]:


start_point = fc.Point(x=0, y=0, z=0)
end_point = fc.Point(x=100, y=0, z=0.1)
steps = fc.segmented_line(start_point, end_point, segments=15)
for step in steps:
    step.y = step.y + 20*sin(tau*step.x/200)
for i in range(len(steps)): 
    steps.insert(i*2+1,fc.PlotAnnotation(label='')) # add blank PlotAnnotations at all points to highlight them in the plot 
steps.append(fc.PlotAnnotation(point=fc.Point(x=50, y=40,z=0), label='points along a segmented line can be modified after creation to form a curve'))
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


# ## II. measurements from points
# 
# functions:
# - distance
# - point_to_polar
# - angleXY_between_3_points

# In[ ]:


pt1, pt2, pt3 = fc.Point(x=0, y=0, z=0), fc.Point(x=0, y=10, z=0), fc.Point(x=10, y=0, z=0)

distance = fc.distance(pt1, pt2)
print('distance between pt1 and pt2: ' + str(distance))

polar_data = fc.point_to_polar(pt2, fc.Point(x=0, y=0, z=0))
print("\n'polar radius' of pt2 relative to x=0,y=0,z=0: " + str(polar_data.radius))
print("'polar angle' of pt2 relative to x=0,y=0,z=0: " + str(polar_data.angle) + ' (radians: 0 to tau)')
print("'polar angle' of pt2 relative to x=0,y=0,z=0: " + str((polar_data.angle/tau)*360) + ' (degrees: 0 to 360)')
# see the creation of a point from polar coordinates elsewhere in this notebook - fc.polar_to_point() 

angle = fc.angleXY_between_3_points(pt1, pt2, pt3)
print('\nangle between pt1-pt2-pt3: ' + str(angle) + ' (radians: -tau to tau)')
print('angle between pt1-pt2-pt3: ' + str((angle/tau)*360) + ' (degrees: -360 to 360)')


# ## III. move and copy points
# 
# the move() function in FullControl allows moving and coping of a point, list of points, or a combined list of points and other ***state***-changing object
# 
# the amount of movement is defined by FullControl's Vector object

# #### move

# In[ ]:


vector = fc.Vector(x=0, y=0, z=0.5)

start_point = fc.Point(x=0,y=0,z=0)
print('start_point: ' + str(start_point))
moved_start_point = fc.move(start_point, vector)
print('moved_start_point: ' + str(moved_start_point))

steps = fc.rectangleXY(start_point, 50, 20)
print('\noriginal points for a rectangle: ' + str(steps))
steps = fc.move(steps, vector)
print('moved rectangle: ' + str(steps))

steps=[start_point,fc.Fan(speed_percent=90),moved_start_point]
print('\nlist with non-point object: ' + str(steps))
print('moved list with non-point object ' + str(fc.move(steps,vector)))


# #### copy

# In[ ]:


vector = fc.Vector(x=0, y=0, z=0.5)
start_point = fc.Point(x=0,y=0,z=0)
steps = fc.rectangleXY(start_point, 50, 20)
steps = fc.move(steps, vector,copy=True, copy_quantity=5)
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


# #### move/copy (polar coordinates)

# In[ ]:


array_centre = fc.Point(x=50,y=50,z=0)
first_helix_centre = fc.Point(x=20, y=50, z=0)
steps = fc.helixZ(first_helix_centre,10,10,0,5,0.5,100)
steps = fc.move_polar(steps, array_centre, 0, tau/6, copy=True, copy_quantity=6)
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


# #### reflect
# 
# points can be reflected about a line that is defined by either two points (fc.reflectXY), or by one point and a polar angle (fc.reflectXYpolar)
# - polar angle convention:
#     - 0 = positive x direction
#     - 0.25*tau = positive y direction
#     - 0.5*tau = negative x direction
#     - 0.75*tau = negative y direction.

# In[ ]:


steps = []

pt1 = fc.Point(x=50, y=50, z=0)
print('point before reflecting: \n' + str(pt1))
pt1_reflected = fc.reflectXY(pt1, fc.Point(x=0, y=0), fc.Point(x=1, y=0))
print("point after reflecting about x-axis using 'reflectXY()': \n" + str(pt1_reflected))
pt1_reflected = fc.reflectXYpolar(pt1, fc.Point(x=0, y=0), tau/4)
print("point after reflecting about y-axis using 'reflect_polar()': \n" + str(pt1_reflected))


# #### reflecting a list
# 
# FullControl's reflect functions can only be used on individual points. reflecting lists of points is not simple because a reflected list of points must typically be printed in reverse order. otherwise, the nozzle would jump from the last point to the first point of the list before printing its reflection. if the list contained instructions halfway through to change ***state*** beyond a point (e.g. turn extrusion on/off), these instructions would affect different sections of the print path for the reflected and non-reflected lists since their sequences are reversed. therefore, FullControl allows the designer to reflect points only - it is up to the designer to iterate through a list of points, as demonstrated below. if ***state***-changing objects are included in the list, it is up to the designer to decide the appropriate location for them in the reflected list and to not attempt a reflectXY() function on them since they will not have xyz attributes

# In[ ]:


steps = []
steps.extend(fc.arcXY(fc.Point(x=50, y=50, z=0), 10, (5/8)*tau, tau/8, 16))
steps.extend(fc.arcXY(fc.Point(x=80, y=55, z=0), 15, 0.75*tau, 0.5*tau, 16))
steps.extend(fc.arcXY(fc.Point(x=80, y=65, z=0), 5, 0.25*tau, 0.5*tau, 16))
steps.extend(fc.arcXY(fc.Point(x=80, y=55, z=0), 5, 0.25*tau, -0.5*tau, 16))
steps.extend(fc.arcXY(fc.Point(x=60, y=60, z=0), 10, 0.75*tau, -tau/8, 16))

steps_and_annotation = steps + [fc.PlotAnnotation(label='this geometry is reflected in next plot')]
fc.transform(steps_and_annotation, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))

steps_reflected = []
step_count = len(steps)
for i in range(step_count):
    # reflect about a line connecting the first point (steps[0]) and last point (steps[-1])
    steps_reflected.append(fc.reflectXY(steps[(step_count-1)-i], steps[0], steps[-1]))
steps.extend(steps_reflected)
steps.extend([fc.PlotAnnotation(point = pt, label='') for pt in fc.segmented_line(fc.Point(x=43, y=43, z=0), fc.Point(x=52.5, y=52.5, z=0), 20)])
# add some points to the plot to indicate the reflection line
steps.append(fc.PlotAnnotation(point=steps[step_count], label='all points from the previous plot were reflected and added to the path (in reverse order)'))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))

#!/usr/bin/env python
# coding: utf-8

# # lab five-axis demo
# 
# this documentation gives a brief overview of 5-axis capabilities - it will be expanded in the future
# 
# most of this tutorial relates to a system with B-C rotation stages, where C-axis rotations do not affect the B axis, but B-axis rotations do alter the C axis orientation (i.e. a rotating stage [C] mounted onto a tilting platform [B])
# 
# the final section of this notebook demosntrates how to generate gcode for a system with a rotating nozzle (B) and rotating bed (C) 
# 
# the generated gcode would work on other 5-axis systems but this would likely require minor tweaks and a good understanding of the gcode requirements
# 
# <*this document is a jupyter notebook - if they're new to you, check out how they work:
# [link](https://www.google.com/search?q=ipynb+tutorial),
# [link](https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb),
# [link](https://colab.research.google.com/)*>
# 
# *run all cells in this notebook in order (keep pressing shift+enter)*

# #### five axis import

# In[ ]:


import lab.fullcontrol.fiveaxis as fc5
import fullcontrol as fc
import lab.fullcontrol as fclab


# #### basic demo
# 
# points are designed in the model's XYZ coordinate system
# 
# the point x=0, y=0, z=0 in the model's coordinate system represents the intercept point of B and C axes
# 
# FullControl translates them to the 3D printer XYZ coordinates, factoring in the effect of rotations to B and C axes
# 
# a full explanation of this concept is out of scope for this brief tutorial notebook - google 5-axis kinematics for more info
# 
# however, the following code cell briefly demonstrates how changes to the model coordinates and orientation affect the machine coordinates in interesting ways 

# In[ ]:


steps=[]
steps.append(fc5.Point(x=0, y=0, z=0, b=0, c=0))
steps.append(fc5.GcodeComment(end_of_previous_line_text='start point'))
steps.append(fc5.Point(x=1))
steps.append(fc5.GcodeComment(end_of_previous_line_text='set x=1 - since b=0 and c=0, the model x-axis is oriented the same as the system x-axis'))
steps.append(fc5.Point(b=45))
steps.append(fc5.GcodeComment(end_of_previous_line_text='set b=45 - this causes a change to x and z in system coordinates'))
steps.append(fc5.Point(b=90))
steps.append(fc5.GcodeComment(end_of_previous_line_text='set b=90 - although x and z change, E=0 because the nozzle stays in the same point on the model'))
steps.append(fc5.Point(b=0))
steps.append(fc5.GcodeComment(end_of_previous_line_text='set b=0'))
steps.append(fc5.Point(c=90))
steps.append(fc5.GcodeComment(end_of_previous_line_text='set c=90 - this causes a change to x and y in system coordinates'))
steps.append(fc5.Point(y=1))
steps.append(fc5.GcodeComment(end_of_previous_line_text='set y=1 - this causes a change to x in system coordinates since the model is rotated 90 degrees'))
print(fc5.transform(steps, 'gcode'))


# #### add custom color to preview axes
# 
# this code cell demonstrates a convenient way to add color for previews - it is not supposed to be a useful print path, it's just for demonstration
# 
# after creating all the steps in the design, color is added to each Point object based on the Point's orientation in B

# In[ ]:


steps = []
steps.append(fc5.Point(x=0, y=0, z=0, b=0, c=0))
steps.append(fc5.PlotAnnotation(label='B0'))
steps.append(fc5.Point(x=10, y=5, z=0, b=0, c=0))
steps.append(fc5.PlotAnnotation(label='B0'))
steps.append(fc5.Point(y=10, z=0, b=-180, c=0))
steps.append(fc5.PlotAnnotation(label='B-180'))
steps.append(fc5.Point(x=0, y=15, b=-180, c=0))
steps.append(fc5.PlotAnnotation(label='B-180'))
steps.append(fc5.Point(y=20, b=180, c=0))
steps.append(fc5.PlotAnnotation(label='B+180'))
steps.append(fc5.Point(x=10, y=25, b=180, c=0))
steps.append(fc5.PlotAnnotation(label='B+180'))
for step in steps:
    if type(step).__name__ == 'Point':
        # color is a gradient from B=-180 (blue) to B=+180 (red)
        step.color = [((step.b+180)/360), 0, 1-((step.b+180)/360)]
fc5.transform(steps, 'plot', fc5.PlotControls(color_type='manual'))


# #### a more complex color example
# 
# this example shows a wavey helical print path, where the model is continuously rotating while the nozzle gradually moves away from the print platform
# 
# the part is tilted to orient the nozzle perpendicular(ish) to the wavey walls at all points

# In[ ]:


from math import sin, cos, tau
steps = []
for i in range(10001):
    angle = tau*i/200
    offset = (1.5*(i/10000)**2)*cos(angle*6)
    steps.append(fc5.Point(x=(6+offset)*sin(angle), y=(6+offset)*cos(angle), z=((i/200)*0.1)-offset/2, b=(offset/1.5)*30, c=angle*360/tau))
for step in steps:
    if type(step).__name__ == 'Point':
        # color is a gradient from B=0 (blue) to B=45 (red)
        step.color = [((step.b+30)/60), 0, 1-((step.b+30)/60)]
steps.append(fc5.PlotAnnotation(point=fc5.Point(x=0, y=0, z=8.75), label='color indicates B axis (tilt)'))
steps.append(fc5.PlotAnnotation(point=fc5.Point(x=0, y=0, z=7.5), label='-30 deg (blue) to +30 deg (red)'))
gcode = fc5.transform(steps,'gcode')
print('final ten gcode lines:\n' + '\n'.join(gcode.split('\n')[-10:]))
fc5.transform(steps, 'plot', fc5.PlotControls(color_type='manual', hide_axes=False, zoom=0.75))


# #### use 3-axis geometry functions from FullControl (with caution!)
# 
# this functionality should be considered experimental at best!
# 
# geometry functions that generate 3-axis points can be used - accessed via fc5.xyz_geom()
# 
# but they must be translated to have 5-axis methods for gcode generation - achieved via fc5.xyz_add_bc()
# 
# this conversion does not set any values of B or C attributes for those points - the BC values will remain at whatever values they were in the ***design*** before the list of converted points
# 
# in the example below, a circle is created in the XY plane in the model's coordinate system, but the b-axis is set to 90
# 
# therefore, the 3D printer actually prints a circle in the YZ plane since the model coordinate system has been rotated by 90 degrees about the B axis
# 
# hence, when the ***design*** is transformed to a 'gcode' ***result***, Y and Z values vary in gcode while X is constant (of course this would not print well - it's just for simple demonstration)
# 
# in contrast, when the ***design*** is transformed to a 'plot' ***result***, the plot shows model coordinates because 5-axis plots in the 3D-printer's coordinates system often make no sense visually

# In[ ]:


steps=[]
steps.append(fc5.Point(x=10, y=0, z=0, b=90, c=0))
xyz_geometry_steps = fc5.xyz_geom.circleXY(fc5.Point(x=0, y=0, z=0), 10, 0, 16)
xyz_geometry_steps_with_bc_capabilities = fc5.xyz_add_bc(xyz_geometry_steps)
steps.extend(xyz_geometry_steps_with_bc_capabilities)
steps.append(fc5.PlotAnnotation(point=fc5.Point(x=0, y=0, z=5), label='normal FullControl geometry functions can be used via fc5.xyz_geom'))
steps.append(fc5.PlotAnnotation(point=fc5.Point(x=0, y=0, z=3.5), label='but points must be converted to 5-axis variants via fc5.xyz_add_bc'))
print(fc5.transform(steps, 'gcode'))
fc5.transform(steps, 'plot')


# #### bc_intercept
# 
# if the machine's coordinate system is **not** set up so that the b and c axes intercept at the point x=0, y=0, z=0, the bc_intercept data can be provided in a GcodeControls object to ensure correct gcode generation
# 
# the GcodeControls object has slightly less functionality for 5-axis FullControl compared to 3-axis FullControl - there are no printer options to choose from at present (the 'generic' printer is always used) and no built-in primer can be used
# 
# note that although the system does not need the b and c axes to intercept at the point x=0, y=0, z=0, the model coordinate system must still be implemented such that the point x=0, y=0, z=0 represents the intercept point of b and c axes

# In[ ]:


gcode_controls = fc5.GcodeControls(bc_intercept = fc5.Point(x=10, y=0, z=0), initialization_data={'nozzle_temp': 250})
steps=[]
steps.append(fc5.Point(x=0, y=0, z=0, b=0, c=0))
steps.append(fc5.GcodeComment(end_of_previous_line_text='start point (x=0 in the model but x=10 in gcode due to the bc_intercept being at x=10)'))
steps.append(fc5.Point(x=1))
steps.append(fc5.GcodeComment(end_of_previous_line_text='set x=1 - since b=0 and c=0, the model x-axis is oriented the same as the system x-axis'))
steps.append(fc5.Point(b=45))
steps.append(fc5.GcodeComment(end_of_previous_line_text='set b=45 - this causes a change to x and z in system coordinates'))
print(fc5.transform(steps, 'gcode', gcode_controls))


# #### rotating-nozzle 5-axis system
# 
# if the nozzle rotates about the Y axis, as opposed to the rotating bed tilting about the Y axis (as was the case for the code above), but the print bed still rotates about the Z axis, you can import `lab.fullcontrol.fiveaxisC0B1` as fc5 instead of ` lab.fullcontrol.fiveaxis`
# 
# this is shown in the code cell below. note that the new import statement means the previous import of fc5 is nullified, so don't try to run the above code cells after running the next code cell or they won't work
# 
# the simple instructions below show how rotation of the bed and of the nozzle independently result in necessary changes to X and Y in gcode
# 
# in the future, the way of defining which type of multiaxis printer you change will be made more intuitive and procedural, but this works for now.

# In[ ]:


import lab.fullcontrol.fiveaxisC0B1 as fc5
b_offset_z = 40
steps=[]
steps.append(fc5.Point(x=0, y=0, z=0, b=0, c=0))
steps.append(fc5.GcodeComment(end_of_previous_line_text='start point'))
steps.extend([fc5.Point(x=1), fc5.GcodeComment(end_of_previous_line_text='x=1')])
steps.extend([fc5.Point(c=90), fc5.GcodeComment(end_of_previous_line_text='c=90')])
steps.extend([fc5.Point(c=180), fc5.GcodeComment(end_of_previous_line_text='c=180')])
steps.extend([fc5.Point(c=270), fc5.GcodeComment(end_of_previous_line_text='c=270')])
steps.extend([fc5.Point(x=0, y=1, c=0), fc5.GcodeComment(end_of_previous_line_text='x=0, y=1, c=0')])
steps.extend([fc5.Point(c=90), fc5.GcodeComment(end_of_previous_line_text='c=90')])
steps.extend([fc5.Point(c=180), fc5.GcodeComment(end_of_previous_line_text='c=180')])
steps.extend([fc5.Point(c=270), fc5.GcodeComment(end_of_previous_line_text='c=270')])
steps.extend([fc5.Point(b=90), fc5.GcodeComment(end_of_previous_line_text='b=90')])
steps.extend([fc5.Point(b=-90), fc5.GcodeComment(end_of_previous_line_text='b=-90')])
print(fc5.transform(steps, 'gcode', fc5.GcodeControls(b_offset_z=b_offset_z)))


# to keep the nozzle directly to the hand side of the bed (Y=0) for every point, which is useful for nozzle tilting about Y when printing a funnel for example, you need to design C to rotate for each point

# In[ ]:


from math import degrees

circle_segments = 16
points_per_circle = circle_segments+1
steps = []
xyz_geometry_steps = fc5.xyz_geom.circleXY(fc5.Point(x=0, y=0, z=0), 10, 0, circle_segments)
xyz_geometry_steps_with_bc_capabilities = fc5.xyz_add_bc(xyz_geometry_steps)
steps.extend(xyz_geometry_steps_with_bc_capabilities)
steps[0].b, steps[0].c = 0.0, 0.0
gcode_without_c_rotation = fc5.transform(steps, 'gcode', fc5.GcodeControls(b_offset_z=b_offset_z))
fc5.transform(steps, 'plot')

for i in range(len(steps)): steps[i].c = -360/circle_segments*i
# instead of the above for loop, you can use the following function to constantly vary c automatically. This is good for more complex geometry, where c cannot be 'designed' easily.
# steps = fclab.constant_polar_angle_with_c(points=steps, centre=fc5.Point(x=0, y=0, z=0), initial_c=-90)
gcode_with_c_rotation = fc5.transform(steps, 'gcode', fc5.GcodeControls(b_offset_z=b_offset_z))

print(gcode_without_c_rotation +
      '\n\n\ngcode with C rotation to keep nozzle directly in +X direction from bed centre:\n\n' + gcode_with_c_rotation)


# #### next steps
# 
# this tutorial notebook gives a brief introduction to five-axis use of FullControl for interest, but it is not an expansive implementation. it is included as an initial step towards translating in-house research for 5-axis gcode generation into a more general format compatible with the overall FullControl concept
#!/usr/bin/env python
# coding: utf-8

# # lab four-axis demo
# 
# this documentation gives a brief overview of 4-axis capabilities - it will be expanded in the future
# 
# it currently works for a system with a nozzle rotating about the y axis, for which open-source documentation will be released soon
# 
# the generated gcode would work on other 4-axis systems but this would likely require minor tweaks and a good understanding of the gcode requirements
# 
# <*this document is a jupyter notebook - if they're new to you, check out how they work:
# [link](https://www.google.com/search?q=ipynb+tutorial),
# [link](https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb),
# [link](https://colab.research.google.com/)*>
# 
# *run all cells in this notebook in order (keep pressing shift+enter)*

# #### four axis import

# In[ ]:


import lab.fullcontrol.fouraxis as fc4


# #### basic demo
# 
# points in fullcontrol are designed in the model's XYZ coordinate system
# 
# rotation of the b axis will cause the nozzle to move in the x and z directions, and the amount that it moves depends on how far the tip of the nozzle is away from the axis of rotation. therefore it is important to set this distance with `GcodeControls(b_offset_z=...)` to allow fullcontrol to determine the correct x z values to send to the printer
# 
# if the nozzle is below the axis of rotation b_offset_z should be positive
# 
# there is also the potential for the nozzle to be offset from the axis of rotation in the x direction when it is vertical (b=0). this is not currently programmed in fullcontrol but will be in the future and will be set by the user with `b_offset_x`
# 
# the GcodeControls object has slightly less functionality for 4-axis FullControl compared to 3-axis FullControl - there are no printer options to choose from at present (the 'generic' printer is always used) and no built-in primer can be used
# 

# In[ ]:


b_offset_z = 46.0 # mm


# the following code cell briefly demonstrates how changes to the model coordinates and orientation affect the machine coordinates in interesting ways 

# In[ ]:


steps=[]
steps.append(fc4.Point(x=0, y=0, z=0, b=0))
steps.append(fc4.GcodeComment(end_of_previous_line_text='start point'))
steps.append(fc4.Point(x=1))
steps.append(fc4.GcodeComment(end_of_previous_line_text='set x=1 - gcode for this is simple... just move in x'))
steps.append(fc4.Point(b=60))
steps.append(fc4.GcodeComment(end_of_previous_line_text='set b=45 - this causes a change to x and z in system coordinates'))
steps.append(fc4.Point(b=90))
steps.append(fc4.GcodeComment(end_of_previous_line_text="set b=90 - although x and z change, the nozzle tip doesn't move (hence E=0)"))
steps.append(fc4.Point(z=1))
steps.append(fc4.GcodeComment(end_of_previous_line_text="set z=1 - just like the x-movement above, this z-movement is simple. it's only changes to nozzle angle that affect other axes"))
steps.append(fc4.Point(b=-90))
steps.append(fc4.GcodeComment(end_of_previous_line_text='set b=-90 - the print head moves to the opposite side when the nozzle rotates 180 degrees to ensure the nozzle stays at x=1'))
print(fc4.transform(steps, 'gcode', fc4.GcodeControls(b_offset_z=b_offset_z)))


# #### add custom color to preview axes
# 
# this code cell demonstrates a convenient way to add color for previews - it is not supposed to be a useful print path, it's just for demonstration
# 
# after creating all the steps in the design, color is added to each Point object based on the Point's orientation in B

# In[ ]:


steps = []
steps.append(fc4.Point(x=0, y=0, z=0, b=0))
steps.append(fc4.PlotAnnotation(label='B0'))
steps.append(fc4.Point(x=10, y=5, z=0, b=0))
steps.append(fc4.PlotAnnotation(label='B0'))
steps.append(fc4.Point(y=10, z=0, b=-180))
steps.append(fc4.PlotAnnotation(label='B-45'))
steps.append(fc4.Point(x=0, y=15, b=-180))
steps.append(fc4.PlotAnnotation(label='B-45'))
steps.append(fc4.Point(y=20, b=180))
steps.append(fc4.PlotAnnotation(label='B+45'))
steps.append(fc4.Point(x=10, y=25, b=180))
steps.append(fc4.PlotAnnotation(label='B+45'))
for step in steps:
    if type(step).__name__ == 'Point':
        # color is a gradient from B=-180 (blue) to B=+180 (red)
        step.color = [((step.b+45)/90), 0, 1-((step.b+45)/90)]
fc4.transform(steps, 'plot', fc4.PlotControls(color_type='manual'))


# #### a more complex color example
# 
# this example shows a wavey helical print path, where the tilts to easy side (oscialtes once per layer)
# 
# the part is tilted to orient the nozzle perpendicular(ish) to the wavey walls at all points

# In[ ]:


from math import sin, cos, tau
EH = 0.4
EW = 1.2

rad = 12  # nominal radius of structure before offsets
max_offset = rad

start_x, start_y = 75, 75
initial_z = 0.5*EH

steps = []
segs, segs_per_layer = 10000, 200
max_z = (segs/segs_per_layer)*EH

for i in range(segs+1):
    angle = tau*i/segs_per_layer
    offset = (max_offset*(i/segs)**2)*(0.5+0.5*cos(angle*2))
    steps.append(fc4.Point(x=start_x+(rad+offset)*cos(angle), y=start_y+(rad+offset)*sin(angle),
                 z=initial_z+((i/segs_per_layer)*EH)-offset/2, b=cos(angle)*(offset/max_offset)*45))
for step in steps:
    if type(step).__name__ == 'Point':
        # color is a gradient from B=-45 (blue) to B=45 (red)
        step.color = [((step.b+45)/90), 0, 1-((step.b+45)/90)]
steps.append(fc4.PlotAnnotation(point=fc4.Point(
    x=start_x, y=start_y, z=max_z*1.2), label='color indicates B axis (tilt)'))
steps.append(fc4.PlotAnnotation(point=fc4.Point(
    x=start_x, y=start_y, z=max_z), label='-45 deg (blue) to +45 deg (red)'))
gcode = fc4.transform(steps, 'gcode', fc4.GcodeControls(b_offset_z=b_offset_z, initialization_data={
                      'print_speed': 500, 'extrusion_width': EW, 'extrusion_height': EH}))
print('final ten gcode lines:\n' + '\n'.join(gcode.split('\n')[-10:]))
fc4.transform(steps, 'plot', fc4.PlotControls(
    color_type='manual', hide_axes=False, zoom=0.75))

design_name = 'fouraxis'
open(f'{design_name}.gcode', 'w').write(gcode)

# activate the next line to download the gcode if using google colab
# files.download(f'{design_name}.gcode')


# #### use 3-axis geometry functions from FullControl (with caution!)
# 
# this functionality should be considered experimental at best!
# 
# geometry functions that generate 3-axis points can be used - accessed via fc4.xyz_geom()
# 
# but they must be translated to have 4-axis methods for gcode generation - achieved via fc4.xyz_add_b()
# 
# this conversion does not set any values of B attributes for those points - the B values will remain at whatever values they were in the ***design*** before the list of converted points
# 
# in the example below, a circle is created in the XY plane in the model's coordinate system, but the b-axis is set to 45
# 
# hence, when the ***design*** is transformed to a 'gcode' ***result***, X and Z values vary from the design X Z values in gcode to accomodate the true required position of the printhead (to get the desired nozzle location)
# 
# in contrast, when the ***design*** is transformed to a 'plot' ***result***, the plot shows model coordinates (e.g. Z=0) because 4-axis plots in the 3D-printer's coordinates system often make no sense visually

# In[ ]:


steps=[]
steps.append(fc4.Point(x=10, y=0, z=0, b=45))
xyz_geometry_steps = fc4.xyz_geom.circleXY(fc4.Point(x=0, y=0, z=0), 10, 0, 16)
xyz_geometry_steps_with_bc_capabilities = fc4.xyz_add_b(xyz_geometry_steps)
steps.extend(xyz_geometry_steps_with_bc_capabilities)
steps.append(fc4.PlotAnnotation(point=fc4.Point(x=0, y=0, z=5), label='normal FullControl geometry functions can be used via fc4.xyz_geom'))
steps.append(fc4.PlotAnnotation(point=fc4.Point(x=0, y=0, z=3.5), label='but points must be converted to 4-axis variants via fc4.xyz_add_b'))
print(fc4.transform(steps, 'gcode', fc4.GcodeControls(b_offset_z=30)))
fc4.transform(steps, 'plot')

#!/usr/bin/env python
# coding: utf-8

# # lab geometry functions
# 
# the FullControl lab exists for things that aren't suitable for the main FullControl package yet, potentially due to complexity in terms of their concept, code, hardware requirements, computational requirements, etc.
#  
# FullControl features/functions/classes in the lab may be more experimental in nature and should be used with caution, with an understanding that they may change in future updates
# 
# at present, both the lab and the regular FullControl packages are under active development and the code and package structures may change considerably. some aspects currently in FullControl may move to lab and vice versa
# 
# lab currently has the following aspects:
# - geometry functions that supplement existing geometry functions in FullControl
# - four-axis and five-axis demos
# - transformation of a fullcontrol ***design*** into a 3D model (stl file) of the designed geometry with extudate heights and widths based on the designed `ExtrusionGeometry` 
# 
# this notebook briefly demonstrates the geometry functions. four-axis, five-axis and 3d-model-output capabilities are demonstrated in their respective noetbooks:
# - [5-axis notebook](lab_five_axis_demo.ipynb)
# - [4-axis notebook](lab_four_axis_demo.ipynb)
# - [stl-output notebook](lab_stl_output.ipynb)

# #### FullControl lab import

# In[ ]:


import fullcontrol as fc
import lab.fullcontrol as fclab
from math import tau, radians


# #### bezier curves

# In[ ]:


bez_points = []
bez_points.append(fc.Point(x=10, y=10, z=0))
bez_points.append(fc.Point(x=10, y=0, z=0))
bez_points.append(fc.Point(x=0, y=10, z=0))
bez_points.append(fc.Point(x=10, y=10, z=0))
bez_points.append(fc.Point(x=9, y=9, z=2))
steps = fclab.bezier(bez_points, num_points=100)
fc.transform(steps, 'plot', fc.PlotControls(style="line", zoom=0.8))


# #### polar sine waves

# In[ ]:


centre = fc.Point(x=0, y=0, z=0)
radius = 10
amplitude = -2
start_angle = 0
arc_angle = radians(270)
periods = 12
segments_per_period = 8
extra_half_period = False
phase_shift = 0
steps = fclab.arc_sinewaveXY(centre, radius, amplitude, start_angle, arc_angle, periods, segments_per_period, extra_half_period, phase_shift)
fc.transform(steps, 'plot', fc.PlotControls(style="line", zoom=0.8, color_type='print_sequence'))


# #### convex (streamline slicing)
# 
# the CONVEX (CONtinuously Varied EXtrusion) approach allows continuously varying extrusion width. i.e. streamline-slicing
# 
# see method images and case study in the associated journal paper [(free download)](https://www.researchgate.net/publication/346098541)
# 
# two outer edges are defined as paths and the CONVEX function fills the space between these edges with the desired number of paths
# 
# to travel between the end of one paths and start of the next, set `travel=True`
# 
# it optionally allows speed to be continuously matched to instantaneous extrusion width to maintain constant volumetric flowrate:
# - set `vary_speed` parameter to be True and supply values for `speed_ref` and `width_ref` parameters
# - these parameters are used to change speed proportional to how wide the instantaneous segment being printed is compared to width_ref
# 
# for open paths, it's useful to print lines using a zigzag strategy to avoid the nozzle moving back to the same side after printing each line - this is achieved by setting `zigzag=True`
# 
# set `overextrusion_percent` to achieve more extrusion while not changing the physical separation of line - this can help ensure good lateral bonding between neighbouring lines 
# 
# it can be used to fill an arbirary shape by setting the 'inner edge' to be a list of coincident points near the centre of the shape. or for shapes with longish aspect ratios, 'inner edge' could be an abritrary list of points going along the appoximate medial axis and back.
# 
# these are example implementations, CONVEX can be used far more broadly

# In[ ]:


outline_edge_1 = fc.circleXY(fc.Point(x=0, y=0, z=0.2), 5, 0, 64)
outline_edge_2 = fc.circleXY(fc.Point(x=1, y=0, z=0.2), 3, 0, 64)
steps = fclab.convex_pathsXY(outline_edge_1, outline_edge_2, 10)
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='tube'))

# to vary speed to maintain constant flow rate:
# steps = fclab.convex_pathsXY(outline_edge_1, outline_edge_2, 10, vary_speed = True, speed_ref = 1000, width_ref = 0.6)


# In[ ]:


outline_edge_1 = fclab.bezier([fc.Point(x=0, y=0, z=0.2), fc.Point(x=10, y=5, z=0.2), fc.Point(x=20, y=0, z=0.2)], num_points = 100)
outline_edge_2 = fclab.bezier([fc.Point(x=0, y=10, z=0.2), fc.Point(x=10, y=5, z=0.2), fc.Point(x=20, y=10, z=0.2)], num_points = 100)
steps = fclab.convex_pathsXY(outline_edge_1, outline_edge_2, 15, zigzag=True, travel=False)
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='tube'))


# instead of printing the above example geometry with lines running from end to end, you could design an imaginary 'outline' running along the medial axis of the specimen
# 
# then the part can be printed it in a similar manner to the ring example above, with lines printed from the outside inwards - there's just no hole in the middle
# 
# this is similar to concentric print paths in slicers, except the lines continuously fluctuate in width to achieve a shape-fitting path, which avoids islands needing to be printed with travel moves in between

# In[ ]:


points = 100
outline_edge_1 = fclab.bezier([fc.Point(x=0, y=0, z=0.2), fc.Point(x=10, y=5, z=0.2), fc.Point(x=20, y=0, z=0.2)], num_points = points)
outline_edge_2_reverse = fclab.bezier([fc.Point(x=20, y=10, z=0.2), fc.Point(x=10, y=5, z=0.2), fc.Point(x=0, y=10, z=0.2)], num_points = points)
inner_edge_1 = fc.segmented_line(fc.Point(x=4, y=5, z=0.2), fc.Point(x=16, y=5, z=0.2), points)
inner_edge_2_reverse = fc.segmented_line(fc.Point(x=16, y=5, z=0.2), fc.Point(x=4, y=5, z=0.2), points)
# create a closed path of the outline
outer_edge = outline_edge_1 + outline_edge_2_reverse + [outline_edge_1[0]]
# create a 'path' along the medial axis with the same number of points as 'outer_edge'
inner_edge = inner_edge_1 + inner_edge_2_reverse + [inner_edge_1[0]]
steps = fclab.convex_pathsXY(outer_edge, inner_edge, 7, travel=False)
steps.append(fc.PlotAnnotation(point = fc.Point(x=10, y=5, z=5), label="the default tube plotting style may not represent sudden changes in widths accurately"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='tube'))
steps[-1] = (fc.PlotAnnotation(point = fc.Point(x=10, y=5, z=5), label="use fc.PlotControls(tube_type='cylinders') to get more accurate representations of printed widths"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='tube', tube_type='cylinders'))


# for arbitrary geometry with width-to-length aspect ratios approximately <2.5, it may be feasible to set the inner 'path' to be a list of identical points at a chosen centre point of the geometry
# 
# this example shows how CONVEX can fluctuate speed automatically to maintain constant volumetric flow rate

# In[ ]:


outer_edge = fclab.bezier([fc.Point(x=0, y=0, z=0), 
                           fc.Point(x=20, y=0, z=0), 
                           fc.Point(x=-10, y=6, z=0), 
                           fc.Point(x=20, y=12, z=0), 
                           fc.Point(x=0, y=12, z=0)], num_points=100)
outer_edge = fc.move_polar(outer_edge, fc.Point(x=0, y=6), 0, tau/2, copy=True, copy_quantity=2)
inner_edge = [fc.Point(x=0, y=6, z=0)]*len(outer_edge)
steps = fclab.convex_pathsXY(outer_edge, inner_edge, 12, travel=True, vary_speed=True, speed_ref=2000, width_ref=0.5)
widths_required = [step.width for step in steps if isinstance(step, fc.ExtrusionGeometry)]
speeds_required = [step.print_speed for step in steps if isinstance(step, fc.Printer)]
print(f'extrusion width varies from {min(widths_required):.2} to {max(widths_required):.2} mm')
print(f'speed varies from {min(speeds_required)} to {max(speeds_required)} mm/min, to maintain constant volumetric flow rate')
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='tube', tube_type='flow'))


# #### solid base
# 
# automatically add solid layers to an existing design for a shell structure with fill_base_simple() or fill_base_full(), which use the convex function
# 
# the layer outline is determined based on the 'segments_per_layer' parameter
# 
# fill_base_simple generates solid fill for the first layer then copies it for subsequent solid layers
# fill_base_full generates solid fill for each layer based on the current layer's outline, which is more computationally demanding, but useful if the model does now have near-vertical walls
# 

# In[ ]:


segments_per_layer = 64
helix_layers = 20
helix_start_rad, helix_end_rad = 5, 5
centre = fc.Point(x=0, y=0, z=0)
helix = fc.helixZ(centre, helix_start_rad, helix_end_rad, 0, helix_layers, 0.2, helix_layers*segments_per_layer)

solid_layers, EW = 5, 0.5
steps = fclab.fill_base_simple(helix, segments_per_layer, solid_layers, EW)
fc.transform(steps, 'plot', fc.PlotControls(style="line", zoom=0.8))
helix_end_rad = 10
helix = fc.helixZ(centre, helix_start_rad, helix_end_rad, 0, helix_layers, 0.2, helix_layers*segments_per_layer)
steps = fclab.fill_base_simple(helix, segments_per_layer, solid_layers, EW)
fc.transform(steps, 'plot', fc.PlotControls(style="line", zoom=0.8))
steps = fclab.fill_base_full(helix, segments_per_layer, solid_layers, EW)
fc.transform(steps, 'plot', fc.PlotControls(style="line", zoom=0.8))


# #### offset a path
# 
# required parameters:
# 
# - points: the supplied path - it must be a list of Point objects only
# - offset: the distance to offset the path
# 
# optional parameters:
# 
# - flip: set True to flip the direction of the offset
# - travel: set True to travel to the offset path without printing
# - repeats: set the number of offsets paths - default = 1
# - include_original: set True to return the original path as well as offset paths
# - arc_outer_corners: set True to make outer corners have arcs (good for acute corners)
# - arc_segments: numbers of segments par arc (if arc_outer_corners == True) - default = 8

# In[ ]:


points = [fc.Point(x=10, y=10, z=0.2), fc.Point(x=15, y=15, z=0.2), fc.Point(x=20, y=10, z=0.2)]
offset = 0.4
steps = fclab.offset_path(points, offset, include_original=True, travel=True)
steps.insert(-2, fc.PlotAnnotation(label="the 'travel' parameter enables travel movements to the start of offset paths"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', zoom=0.7, tube_type='cylinders'))


# In[ ]:


points = [fc.Point(x=10, y=10, z=0.2), fc.Point(x=15, y=15, z=0.2), fc.Point(x=20, y=10, z=0.2), fc.Point(x=10, y=10, z=0.2)]
offset = 0.4
steps = fclab.offset_path(points, offset, include_original=True, travel=True)
steps.append(fc.PlotAnnotation(label="the offset path for a closed path is automatically closed too"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', zoom=0.8, tube_type='cylinders'))


# In[ ]:


points = [fc.Point(x=10, y=10, z=0.2), fc.Point(x=15, y=15, z=0.2), fc.Point(x=20, y=10, z=0.2), fc.Point(x=10, y=10, z=0.2)]
offset = 0.4
steps = fclab.offset_path(points, offset, travel=True, repeats=3, include_original=True)
steps.insert(-2, fc.PlotAnnotation(label="path repeated multiple times using the 'repeat' parameters"))
points2 = fc.move(points, fc.Vector(y=-7.5))
steps.extend(fc.travel_to(fc.Point(x=10, y=2.5)))
steps.extend(fclab.offset_path(points2, offset, travel=True, repeats=3, include_original=True, flip=True))
steps.insert(-2, fc.PlotAnnotation(label="path offset direction flipped using the 'flip' parameter"))
fc.transform(steps, 'plot',fc.PlotControls(color_type='print_sequence', zoom=0.8, tube_type='cylinders'))


# In[ ]:


points = [fc.Point(x=10, y=10, z=0.2), fc.Point(x=15, y=15, z=0.2), fc.Point(x=20, y=10, z=0.2), fc.Point(x=10, y=10, z=0.2)]
offset = 0.4
steps = fclab.offset_path(points, offset, repeats=10, travel = True, include_original=True, arc_outer_corners=True, arc_segments=16)
steps.append(fc.PlotAnnotation(label="add radii to corners with 'arc_outer_corners' and 'arc_segments' parameters"))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', tube_type='flow'))


# #### reflect a list of points
# 
# reflecting a list of points is complicated by the fact that the order in which controls are applied (e.g. to turn extrusion on or off) needs careful consideration - see more details about this in the regular [geometry functions notebook](geometry_functions.ipynb)
# 
# the following command can be used to reflect a list of points if it only contains points

# In[ ]:


steps = [fc.Point(x=0, y=0, z=0), fc.Point(x=1, y=1, z=0)]
steps += fclab.reflectXYpolar_list(steps, fc.Point(x=2, y=0, z=0), tau/4)
for step in steps: print(step)


# #### find line intersection
# 
# methods to find the intersection or to check for intersection between lines are demonstrated in the following code cell

# In[ ]:


line1 = [fc.Point(x=0, y=0, z=0), fc.Point(x=1, y=1, z=0)]
line2 = [fc.Point(x=1, y=0, z=0), fc.Point(x=0, y=1, z=0)]
intersection_point = fclab.line_intersection_by_points_XY(line1[0], line1[1], line2[0], line2[1])
print(f'\ntest 1... intersection at Point: {intersection_point}')

line_1_point = fc.Point(x=0, y=1, z=0)
line_1_angle = 0
line_2_point = fc.Point(x=1, y=0, z=0)
line_2_angle = tau/4
intersection_point = fclab.line_intersection_by_polar_XY(line_1_point, line_1_angle, line_2_point, line_2_angle)
print(f'\ntest 2... intersection at Point: {intersection_point}')

line1 = [fc.Point(x=0, y=0, z=0), fc.Point(x=1, y=1, z=0)]
line2 = [fc.Point(x=1, y=0, z=0), fc.Point(x=0, y=1, z=0)]
intersection_check = fclab.crossing_lines_check_XY(line1[0], line1[1], line2[0], line2[1])
print(f'\ntest 3... intersection between lines (within their length): {intersection_check}')


# #### loop between lines
# 
# 'loop_between_lines' allows smooth continuous printing between two lines - particularly useful for printing sacrificial material outside the region of interest for tissue engineering lattices, etc.

# In[ ]:


line1 = [fc.Point(x=0, y=0, z=0.2), fc.Point(x=0, y=10, z=0.2)]
line2 = [fc.Point(x=10, y=10, z=0.2), fc.Point(x=20, y=0, z=0.2)]
loop_extension = 10 # dictates how far the loop extends past the lines
loop_linearity = 0 # 0 to 10 - disctates how linearly the loop initially extends beyond the desired lines
loop = fclab.loop_between_lines(line1[0], line1[1], line2[0], line2[1], loop_extension, travel=True, num_points=20, linearity=loop_linearity)
steps = line1 + loop + line2
fc.transform(steps, 'plot')


# #### spherical coordinates
# 
# spherical coordinates can be be used to define points with the fclab.spherical_to_point function

# In[ ]:


point = fclab.spherical_to_point(origin = fc.Point(x=100, y=0, z=0), radius = 1, angle_xy=radians(90), angle_z = radians(0))
print(f'fclab.spherical_to_point() for angle_xy=90 degrees, angle_z = 0 degrees: \n    {repr(point)}')
point = fclab.spherical_to_point(origin = fc.Point(x=100, y=0, z=0), radius = 1, angle_xy=radians(90), angle_z = radians(45))
print(f'fclab.spherical_to_point() for angle_xy=90 degrees, angle_z = 45 degrees: \n    {repr(point)}')
point = fclab.spherical_to_point(origin = fc.Point(x=100, y=0, z=0), radius = 1, angle_xy=radians(90), angle_z = radians(90))
print(f'fclab.spherical_to_point() for angle_xy=90 degrees, angle_z = 90 degrees: \n    {repr(point)}')


# fclab.spherical_to_vector is similar to fclab.spherical_to_point but does not need an origin to be defined since vectors can be considered to always be relative to xyz=0
# 
# the 'radius' parameter has also been replaced by the more logical term 'length' 

# In[ ]:


point = fclab.spherical_to_vector(length=10, angle_xy=radians(90), angle_z=radians(45))
print(f'fclab.spherical_to_vector() for angle_xy=90 degrees, angle_z = 45 degrees: \n    {repr(point)}')


# fullcontrol also has functions to determine spherical angles and radius from two points using fclab.point_to_spherical()

# In[ ]:


point1 = fc.Point(x=10, y=0, z=0)
point2 = fc.Point(x=10, y=0, z=10)
spherical_data = fclab.point_to_spherical(origin_point=point1, target_point=point2)
print(f'fclab.point_to_spherical() returns:\n    {repr(spherical_data)}')
angleZ_data = fclab.angleZ(start_point=point1, end_point=point2)
print(f'fclab.angleZ() returns:\n    {repr(angleZ_data)}')

recreated_point2 = fclab.spherical_to_point(point1,spherical_data.radius, spherical_data.angle_xy, spherical_data.angle_z)
print(f'recreated point 2 using spherical data:\n    {repr(point2)}')


# #### 3D rotation
# 
# rotate the toolpath or sections of the toolpath in 3D with fclab.rotate()
# 
# the function requires:
# - list of points
# - start point for the axis or rotation
# - end point for the axis of rotation (or 'x', 'y', or 'z')
# - angle of rotation
# - similar to fc.move(), if multiple copies are required:
#     - copy = True
#     - copy_quantity = number desired (including original)

# In[ ]:


steps = fc.circleXY(fc.Point(x=10,y=0,z=0), 5,0)
steps = fclab.rotate(steps,fc.Point(x=30,y=0,z=0), 'y', tau/200, copy=True, copy_quantity=75)
fc.transform(steps, 'plot', fc.PlotControls(zoom=0.7))


# In[ ]:


start_rad, end_rad, EH = 3, 1, 0.4

bez_points = [fc.Point(x=0, y=0, z=0), fc.Point(x=0, y=0, z=10), fc.Point(x=10, y=0, z=10),
              fc.Point(x=10, y=0, z=20), fc.Point(x=0, y=0, z=20), fc.Point(x=-10, y=0, z=20)]
layers = int(fc.path_length(fclab.bezier(bez_points, 100))/EH)  # use 100 points to calculate bezier path length, then divide by extrusion height to get the number of layers
centres = fclab.bezier(bez_points, layers)

radii = fc.linspace(start_rad, end_rad, layers) 
segment_z_angles = [fclab.angleZ(point1, point2) if point2.x > point1.x else -fclab.angleZ(point1, point2)
                    for point1, point2 in zip(centres[:-1], centres[1:])]
angles = segment_z_angles + [segment_z_angles[-1]]  # last point has now segment after it, so use the angle of the previous segment

steps = []
for layer in range(layers):
    circle = fc.circleXY(centres[layer], radii[layer], 0, 64)
    circle = fclab.rotate(circle, centres[layer], 'y', angles[layer])
    steps.extend(circle + [fc.PlotAnnotation(point=centres[layer], label='')])

fc.transform(steps, 'plot', fc.PlotControls(style='line', zoom=0.4, color_type='print_sequence'))

#!/usr/bin/env python
# coding: utf-8

# # lab stl output
# 
# in addition to transforming a fullcontrol ***design*** into a 'plot' ***result*** or a 'gcode' ***result***, it can also be transformed into a '3d_model' ***result*** - that is a 3D model (e.g. stl file) of the simulated as-printed geometry based on `Point` and `ExtrusionGeometry` objects in the ***design*** 
# 
# this notebook briefly demonstrates how the 3D model can be generated

# #### FullControl lab import

# In[ ]:


import fullcontrol as fc
import lab.fullcontrol as fclab


# #### create a ***design***

# In[ ]:


EW, EH = 0.8, 0.3 # extrusion width and height
radius, layers = 10, 5
design_name = 'test_design'
steps = fc.helixZ(fc.Point(x=0, y=0, z=EH), radius, radius, 0, layers, EH, layers*32)


# ##### transform the design to a 'plot' ***result*** to preview it

# In[ ]:


fc.transform(steps, 'plot', fc.PlotControls(style='tube', zoom=0.7,
             initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))


# ##### ModelControls adjust how a ***design*** is transformed into a '3d_model' ***result***
# 
# ***designs*** are transformed into a 'plot' according to some default settings which can be overwritten with a `PlotControls` object with the following attributes (all demonstrated in this notebook):
# 
# - `stl_filename` - string for filename (do not include '.stl')
# - `include_date` - options: True/False (include dates/time-stamp in the stl filename)
# - `tube_shape` - options: 'rectangle' / 'diamond' / 'hexagon' / 'octagon'  - adjusts cross sectional shape of extrudates in the stl file
#     - note this is a slightly different format than that used when generating 3D plots using `tube-sides` in a `PlotControls` object
# - `tube_type` - options: 'flow'/'cylinders' - adjust how the plot transitions from line to line
#     - see the `PlotControls` tutorial for more info about this parameter
# - `stl_type` - options: 'ascii'/'binary' - stl file format
# - `stls_combined` - options: True/False - state whether ***designs*** containing multiple bodies are saved with all bodies in a single stl file - multiple bodies occur if the ***design*** includes non-extruding-travel moves between extruded regions
# - `initialization_data` - define initial width/height of 3D lines with dictionary: {'extrusion_width': value, 'extrusion_height': value} - these values are used until they are changed by an `ExtrusionGeometry` object in the ***design***

# In[ ]:


fclab.transform(steps, '3d_model', fclab.ModelControls(
    stl_filename=design_name, 
    include_date=False, 
    tube_shape='rectangle',
    tube_type= 'flow', 
    stl_type = 'ascii', 
    stls_combined = True, 
    initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))


# #### colab
# 
# if using google colab, the stl file can be downloaded from the file browser on the left-hand side or with:
# 
# ```
# from google.colab import files
# files.download(f'{design_name}.stl')
# ```
# (assuming `include_date` is False)
#!/usr/bin/env python
# coding: utf-8

# # other FullControl functions
# 
# these other functions support the design process in a range of ways
# 
# they do not give exhaustive functionality, but highlight some useful concepts
# 
# for advanced design, you will likely create new custom functions that do things like these
# 
# <*this document is a jupyter notebook - if they're new to you, check out how they work:
# [link](https://www.google.com/search?q=ipynb+tutorial),
# [link](https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb),
# [link](https://colab.research.google.com/)*>
# 
# *run all cells in this notebook in order (keep pressing shift+enter)*

# In[ ]:


import fullcontrol as fc


# #### fc.linspace()
# 
# linspace is a common function included in numpy and other libraries
# 
# it creates a list of evenly spaced numbers between defined start and end numbers
# 
# it's been created in FullControl to reduce the need to import other packages
# 
# ```
# linspace(start, end, number of points)
# ```

# In[ ]:


print(fc.linspace(1.5,2.5,11))


# #### travel to a point with fc.travel_to()
# 
# in addition to turning the extruder on and off directly with an Extruder object, the 'travel_to' function can be used for the specific case of turning extrusion off, moving to a single point, then turning extrusion on
# 
# this function returns a list of three steps: [Extruder(on=False), Point, Extruder(on=True)]
# 
# since it returns a list, extend() must be used instead of append() when adding the returned steps to an existing list of steps
# 
# if a list of steps is supplied to the function, the first point in the list is used

# In[ ]:


steps_layer_1 = [fc.Point(x=0, y=0, z=0), fc.Point(x=5, y=20), fc.Point(x=10, y=0)]
steps_layer_2 = [fc.Point(x=0, y=0, z=0.4), fc.Point(x=5, y=20), fc.Point(x=10, y=0)]
steps = steps_layer_1 + fc.travel_to(steps_layer_2) + steps_layer_2
steps.extend(fc.travel_to(fc.Point(z=5)))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence'))


# #### define relative points with fc.relative_point()
# 
# define a new point relative to a reference point. this only works if all of x y z attributes are defined for the reference point. it is possible to supply a reference list instead of a reference point, in which case the function uses the last point in the list as the reference point 
# 
# see the [design tips tutorial](design_tips.ipynb) for a way to define absolute points (P) and relative points (R) extremely concisely with *steps.append(****P****(x,y,z))* and *steps.append(****R****(x,y,z))* respectively

# In[ ]:


steps = [fc.Point(x=50, y=50, z=0.2), fc.Point(x=50, y=60, z=0.2)]
steps.append(fc.relative_point(steps[-1], 10, 0, 0))
steps.append(fc.relative_point(steps, 0, -10, 0))
# to be extra concise, assign the the relative_point function to R
for step in steps: print(step)


# #### check a design with fc.check()
# 
# this function can be used to check a design. the current implementation of this function simply summarises the objects in the design and checks that you haven't accidentally added a list of objects as a single entry in the design. the example below shows how this mistake is easy to make if you used append() instead of extend() when adding a list of extra steps to an existing list of steps

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.Extruder(on=False))
steps.append(fc.Point(x=10))
steps.append(fc.Extruder(on=False))
steps.append(fc.Fan(speed_percent=85))
steps.append(fc.Point(x=20))
print('check 1:')
fc.check(steps)
steps.extend(fc.rectangleXY(fc.Point(x=20, y=0, z=0), x_size=10, y_size=10)) # fc.rectangleXY() returns a list of five points
print('\ncheck 2 (extended steps with a list):')
fc.check(steps)
steps.append(fc.rectangleXY(fc.Point(x=20, y=0, z=0), x_size=10, y_size=10))
print('\ncheck 3: (appended steps with a list)')
fc.check(steps)


# #### flatten a ***design*** that contains lists of objects with fc.flatten()
# 
# FullControl ***designs*** must be 1D arrays of FullControl objects. however, it might be conceptually useful to create a ***design*** as a list of actions, where each action may be formed of several steps. if so, you can use fc.flatten to turn a collection of lists into a 1D list

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append([fc.Point(x=10, y=10), fc.ManualGcode(text="G4 P2000 ; pause for 2 seconds")])
steps.append([fc.Point(x=20, y=20), fc.ManualGcode(text="G4 P2000 ; pause for 2 seconds")])
steps.append([fc.Point(x=30, y=30), fc.ManualGcode(text="G4 P2000 ; pause for 2 seconds")])
print('original steps:')
for step in steps:
    print(repr(step))

print("\noriginal steps 'check':")
fc.check(steps)

flat_steps = fc.flatten(steps)
print('\nflat steps:')
for step in flat_steps:
    print(repr(step))
print("\nflat steps 'check':")
fc.check(flat_steps)


# #### find the first or last point in a ***design*** with fc.first_point() and fc.last_point() 
# 
# these functions find the first or last point objects in the design
# 
# it can be set to find the first/last point object of any kind or the first/last one with all of x y z defined

# In[ ]:


steps = [fc.Fan(speed_percent=75), fc.Point(x=1), fc.Point(y=3), fc.Point(x=1, y=1, z=1), fc.Point(x=1, y=1, z=2), fc.Point(x=2), fc.Fan(speed_percent=100)]
print("first step in the design: " + str(type(steps[0]).__name__))
print("first point in the design (not fully defined): " + str(fc.first_point(steps, fully_defined=False)))
print("first point in the design (fully defined): " + str(fc.first_point(steps, fully_defined=True)))
print("last point in the design (not fully defined): " + str(fc.last_point(steps, fully_defined=False)))
print("last point in the design (fully defined): " + str(fc.last_point(steps, fully_defined=True)))


# #### extract points from a ***design*** with fc.point_only()
# 
# this function removes all objects from the ***design*** except Point objects
# 
# it's useful for creating plots or analyzing the geometry, etc.
# 
# it can return fully defined points (all of x y z defined - carried over from previous points if not set by the user) or it can return the points exactly as they were created

# In[ ]:


steps = [fc.Point(x=1, y=1, z=0), fc.Fan(speed_percent=75), fc.Point(y=3)]
print("steps: " + str(steps))
print("points in steps (no tracking): " + str(fc.points_only(steps, track_xyz=False)))
print("points in steps (tracking): " + str(fc.points_only(steps, track_xyz=True)))


# #### export and import a ***design*** as a .json file
# 
# the export_design() exports a ***design*** to a .json file. 
# 
# the import_design() function loads the design back into python. it must be passed the FullControl module handle (fc in this notebook) so it can convert the .json file into the correct type of FullControl objects
# 
# importing a ***design*** is useful if it is computationally demanding to generate the python list of FullControl objects. by exporting a design, you can import it and resume work without needing to repeat the computations/calculations

# In[ ]:


steps = [fc.Point(x=0, y=0, z=0), fc.Point(x=10), fc.Extruder(on=False), fc.Fan(speed_percent=75), fc.Point(x=20)]
fc.export_design(steps, 'my_design')
steps_imported = fc.import_design(fc, 'my_design')
print(fc.transform(steps_imported, 'gcode'))


# #### bounding box
# 
# find the bounding box of a design, including data for min, mid, max and range for x/y/z

# In[ ]:


steps = [fc.Point(x=0,y=0,z=0), fc.Point(x=10,y=10,z=10)]
bounding_box = fc.BoundingBox()
bounding_box.calc_bounds(steps)
print(bounding_box)

#!/usr/bin/env python
# coding: utf-8

# # FullControl overview
# 
# FullControl is used to design changes to the ***state*** of ***things***
# 
# - ***state*** is any property of interest that can change (position, speed, power, temperature, etc.)
# 
# - ***things*** are anything with ***state*** - this initial release of FullControl is focused on ***things*** being extrusion 3D printers that are instructed by gcode
# 
# gcode is a list of instructions that change the ***state*** of a ***thing*** (3D printer, laser cutter, etc.)
# 
# a FullControl ***design*** dictates how the ***states*** of ***things*** change during a procedure (e.g. a manufacturing procedure)
# 
# for this release, the FullControl ***design*** is a 1D list of sequential 'steps' to change ***state***. The designer creates simple python code to generate the list. Each 'step' in the list is created using pre-defined templates for objects built into FullControl (described in later tutorial notebooks)
# 
# FullControl inspects the ***design*** and converts it into a ***result***
# 
# a ***result*** is gcode or a 3D plot in this initial release, but future releases will allow different types of ***designs*** and ***results***. 
# - e.g. to FEA simulations
# - e.g. to documentation to support certification
# 
# at present, gcode can be formatted for a selection of printers and the 3D plot is implemented in plotly, but the range of printers is intended to be extended along with plotting software options
# 
# FullControl contains a set of tools to guide and support the generation of the ***design*** and the ***result***. e.g. geometry functions to support the generation of the ***design***. e.g. different variants of the gcode ***result*** to suit different printers
# 
# <*this document is a jupyter notebook - if they're new to you, check out how they work:
# [link](https://www.google.com/search?q=ipynb+tutorial),
# [link](https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb),
# [link](https://colab.research.google.com/)*>
# 
# *run all cells in this notebook in order (keep pressing shift+enter)*

# # scope of this notebook
# 
# this notebook gives a brief overview of FullControl capabilities with minimal technical explanations
# 
# other tutorial notebooks give full details of the FullControl features demonstrated here

# ## I - import the FullControl python package
# 
# this gives you access to FullControl's functions and objects, etc.
# 
# make sure FullControl is installed first (very simple) - see the [github readme](https://github.com/FullControlXYZ/fullcontrol) for instructions

# In[ ]:


import fullcontrol as fc


# ## II - create a FullControl ***design***
# 
# as described above, the ***design*** is a list of steps using pre-defined FullControl objects as templates for ***state***-changes 
# 
# minimal python knowledge is required
# 
# this notebook introduces basic python features/functions including 1D arrays (*'lists'*), *'append'* and *'extend'* functions, for-loops and the *'math'* module
# 
# complex FullControl designs can be created with only these functions

# #### the ***design*** is a list of steps
# 
# in this example, we create a three-step 'design' 
# each step uses a FullControl 'Point' object, which tells the printer where to move to

# In[ ]:


point_1 = fc.Point(x=10, y=10, z=0)
point_2 = fc.Point(x=20, y=10, z=0)
point_3 = fc.Point(x=10, y=20, z=0)
steps = [point_1, point_2, point_3]


# #### transform the ***design*** into a 'gcode' ***result***
# 
# use the fc.transform() function to transform the list of steps into gcode, then use the print() function to print the gcode to screen
# 
# saving gcode to a .gcode file directly is demonstrated later in this notebook

# In[ ]:


steps = [point_1, point_2, point_3]
gcode = fc.transform(steps, 'gcode', fc.GcodeControls(printer_name='generic'), show_tips=False)
print(gcode)


# #### use the python 'append' and 'extend' functions to add steps to a ***design***

# In[ ]:


# first, create an empty list
steps = []

# then add single items to it with 'append'
steps.append(fc.Point(x=10, y=10, z=0))
steps.append(fc.Point(x=20))
steps.append(fc.Point(x=10, y=20))

# to add multiple items to the list use 'extend'
extra_steps = [fc.Point(x=50, y=50),fc.Point(x=60, y=60),fc.Point(x=70, y=70)]
steps.extend(extra_steps)

# transform the design to gcode and print to screen
print(fc.transform(steps, 'gcode', show_tips=False))


# #### use a python loop to concisely add steps to a ***design***

# In[ ]:


steps = []
for i in range(11):
    steps.append(fc.Point(x=10+i,y=10+i,z=0))
print(fc.transform(steps, 'gcode', show_tips=False))


# #### transform a ***design*** into a 'plot' ***result***
# 
# plot are created from the ***design*** data. it does **not** inspect and plot a gcode file. this means it can utilize design data that may not be included in gcode (e.g. color)
# 
# info about changing the style of the plot (colors, axes, etc.) can be found in a [plot formatting notebook](plot_controls.ipynb)
# 
# the following design loops 25 times to achieve 25 layers with 4 points in each

# In[ ]:


layer_height = 0.2
steps = []
for i in range(25):
    steps.append(fc.Point(x=50,y=55,z=i*layer_height))
    steps.append(fc.Point(x=55+i*layer_height/2,y=50,z=i*layer_height/2))
    steps.append(fc.Point(x=50,y=45,z=i*layer_height))
    steps.append(fc.Point(x=45-i*layer_height/2,y=50,z=i*layer_height/2))
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


# #### use mathematical design to make complex print paths
# 
# this design creates a helix print path that fluctuates in height and radius
# 
# the tau, sin and cos functions need to be imported from python's built-in math module 

# In[ ]:


from math import sin, cos, tau
steps = []
for i in range(10000):
    angle = tau*i/200
    offset = (1.5*(i/10000)**2)*cos(angle*6)
    steps.append(fc.Point(x=(6+offset)*sin(angle), y=(6+offset)*cos(angle), z=((i/200)*0.1)-offset/2))
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


# #### use python *'list comprehension'* to create the list of steps efficiently

# In[ ]:


from random import random
steps = [fc.Point(x=50*random(),y=50*random(),z=i*0.01) for i in range(1000)]
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


# ## III - common types of ***state***

# you can change the ***state*** of more than the nozzle position
# 
# a few examples are shown here - more details about the various types of ***state*** are given in the [state objects notebook](state_objects.ipynb)
# 
# some changes to ***state*** result in a new line of gcode (e.g. changing fan speed)
# 
# other changes do not, but influence future lines of gcode (e.g. changing print speed only manifests in gcode when the next G1 movement command occurs) 

# #### e.g. print speed, fan speed and hotend temperature

# In[ ]:


steps = []
steps.append(fc.Point(x=0,y=0,z=0))
steps.append(fc.Point(x=20))
steps.append(fc.Point(x=40))
steps.append(fc.Printer(print_speed=750))
steps.append(fc.Point(x=60))
steps.append(fc.Point(x=80))
steps.append(fc.Fan(speed_percent=50))
steps.append(fc.Hotend(temp=205))
steps.append(fc.Point(x=100))
print(fc.transform(steps, 'gcode', show_tips=False))


# #### turn the extruder off and on

# In[ ]:


steps = []
steps.append(fc.Point(x=0,y=0,z=0.2))
steps.append(fc.Point(x=5, y=20))
steps.append(fc.Point(x=10, y=0))
steps.append(fc.Extruder(on=False))
steps.append(fc.Point(x=0,y=0,z=0.4))
steps.append(fc.Extruder(on=True))
steps.append(fc.Point(x=5, y=20))
steps.append(fc.Point(x=10, y=0))
steps.extend(fc.travel_to(fc.Point(x=0,y=0,z=0.6)))
steps.append(fc.Point(x=5, y=20))
steps.append(fc.Point(x=10, y=0))
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


# ## IV - annotations and custom commands

# #### add comments for the gcode ***result***

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.GcodeComment(text='the next line of gcode will print to x=20'))
steps.append(fc.Point(x=20))
steps.append(fc.Point(x=40))
steps.append(fc.GcodeComment(end_of_previous_line_text='this line of gcode prints to x=40'))
print(fc.transform(steps, 'gcode', show_tips=False))


# #### add custom gcode commands
# 
# gcode commands can be manually written
# 
# alternatively, the printer has a list of commands that can be called by their id, which allows automatic conversion of commands for different printers' gcode styles

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.Point(x=20))
steps.append(fc.ManualGcode(text="G4 P2000 ; pause for 2 seconds"))
steps.append(fc.PrinterCommand(id='retract'))
print(fc.transform(steps, 'gcode', show_tips=False))


# #### add annotations to the 'plot' ***result***
# 
# more details about plot annotations can be found in the [plot formatting notebook](plot_controls.ipynb)

# In[ ]:


steps = []
for i in range(3):
    steps.append(fc.Fan(speed_percent=50*i))
    for j in range (3):
        steps.append(fc.Point(x=20, y=20+5*j+30*i, z=0+0.1*j))
        steps.append(fc.PlotAnnotation(label="Height: " + str(0+0.1*j) + " mm"))
        steps.append(fc.Point(x=50, y=20+5*j+30*i, z=0+0.1*j))
    steps.append(fc.PlotAnnotation(label="Fan speed: " + str(50*i) + "%"))
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


# ## V - adjust the way the ***design*** is converted into the ***result***

# ### 1. *GcodeControls* adjust gcode creation
# 
# some examples are given below
# 
# for more info about gcode controls, see the [gcode formatting notebook](gcode_controls.ipynb)

# #### save gcode to file
# 
# run the next cell to save gcode as a file in the same folder as this jupyter notebook

# In[ ]:


steps = [fc.Point(x=10, y=10, z=0), fc.Point(x=20), fc.Point(y=20)]
fc.transform(steps, 'gcode', fc.GcodeControls(save_as="my_design"))


# #### change initial print settings
# 
# in addition to changing the ***state*** during the printing process, as shown in the above examples, you can set the ***state*** of initial print settings

# In[ ]:


steps = [fc.Point(x=10, y=10, z=0), fc.Point(x=20), fc.Point(y=20)]
print('########\n######## Default initial conditions:\n########')
print(fc.transform(steps, 'gcode', show_tips=False))
gcode_controls = fc.GcodeControls(initialization_data={"print_speed": 600, "travel_speed": 5750})
print('\n########\n######## Modified initial conditions (see F8000 changed to F5750 and F1000 changed to F600):\n########')
print(fc.transform(steps, 'gcode', gcode_controls, show_tips=False))


# #### change format of gcode ***result*** for different printers
# 
# running the code in the next cell will generate gcode for two different printers and print the first 8 lines to screen

# In[ ]:


steps = [fc.Point(x=10, y=10, z=0), fc.Point(x=20), fc.Point(y=20)]
prusa_gcode = fc.transform(steps, 'gcode', fc.GcodeControls(printer_name='prusa_i3', initialization_data={'relative_e': False}), show_tips=False)
ulti2plus_gcode = fc.transform(steps, 'gcode', fc.GcodeControls(printer_name='ultimaker2plus', initialization_data={'relative_e': True}), show_tips=False)

print('########\n######## prusa gcode - first 8 lines:\n######## ')
gcode_list = (prusa_gcode.split('\n'))
print('\n'.join(gcode_list[0:8]))

print('\n\n########\n######## ultimaker gcode - first 8 lines:\n######## ')
gcode_list = (ulti2plus_gcode.split('\n'))
print('\n'.join(gcode_list[0:8]))


# ### 2. *PlotControls* adjust how plot data is created and displayed
# 
# #### output the raw plot data for use in alternative plottings modules/software
# 
# it's also possible to change color, line-width, etc. - for more info about plot controls, see the [plot formatting notebook](plot_controls.ipynb)
# 
# the next code cell prints the raw plot data to screen and also creates the associated 3D plot for comparison

# In[ ]:


plot_controls = fc.PlotControls(raw_data=True)
steps = [fc.Point(x=10, y=10, z=0), fc.Point(x=30, z=0.5), fc.Point(x=10, z=1), fc.PlotAnnotation(label="End")]
plot_data = fc.transform(steps, 'plot', plot_controls)
print(plot_data)
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


# ## VI - use FullControl geometry functions to create the ***design***
# 
# a few demo functions are shown here - for more details about geometry functions, see the [geometry functions notebook](geometry_functions.ipynb)

# #### e.g. rectangle

# In[ ]:


steps = fc.rectangleXY(fc.Point(x=0, y=0, z=0.2), 20, 4)
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='line'))


# #### e.g. copy geometry to make a linear array

# In[ ]:


steps = fc.rectangleXY(fc.Point(x=0, y=0, z=0.2), 20, 4)
steps = fc.move(steps,fc.Vector(z=0.2),copy=True, copy_quantity=25)
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


# #### e.g. helix

# In[ ]:


centre_point = fc.Point(x=50, y=50, z=0)
steps = fc.helixZ(centre_point, 8, 6, 0, 30, 0.15, 20*64)
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


# #### combine geometry functions to quickly achieve interesting print paths
# - create a squarewave
# - copy it with 180-degree rotation
# - repeat it for 25 layers

# In[ ]:


steps = fc.squarewaveXY(fc.Point(x=20, y=50, z=0), fc.Vector(x=1, y=0), 10, 5, 10)
steps = fc.move_polar(steps,fc.Point(x=67.5, y=45, z=0), 0, tau/2, copy=True)
steps = fc.move(steps, fc.Vector(z=0.2), copy=True, copy_quantity=60)
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


# #### design in polar coordinates
# 
# the FullControl 'polar_to_point' function converts polar coordinates into Cartesian points
# 
# combining it with python's built-in 'list comprehension' capabilities allows a complex list of steps to be created with one line of code

# In[ ]:


steps=[fc.polar_to_point(centre=fc.Point(x=0, y=0, z=i*0.001), radius=10+5*random(), angle=i*tau/13.8) for i in range(4000)]
fc.transform(steps, 'plot', fc.PlotControls(neat_for_publishing=True, zoom=0.7, style='line'))


# #### create custom geometry functions
# 
# the next example is similar to the earlier squarewave example, except it uses a **custom** triangle wave function instead of a function built into FullControl
# 
# if you create useful geometry functions, add them to FullControl so everyone can benefit (see contribution guidelines on [github](https://github.com/FullControlXYZ/fullcontrol))

# In[ ]:


def tri_wave(start_point: fc.Point, amplitude: float, period_length: float, periods: int) -> list:
    tri_wave_steps = []
    for i in range(periods*2+1):
        tri_wave_steps.append(fc.Point(x=start_point.x+i*period_length/2, y=start_point.y+amplitude*(i % 2), z=start_point.z))
    return tri_wave_steps

steps = tri_wave(fc.Point(x=20, y=50, z=0), 10, 10, 10)
steps.extend(tri_wave(fc.Point(x=120, y=40, z=0), -10, -10, 10))
steps = fc.move(steps, fc.Vector(z=0.2), copy=True, copy_quantity=60)
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


# ## VII - next steps
# 
# enhanced functionality has been developed for in-house research and is intended for public release as time allows:
# - multi-axis
#     - full walk-through documentation for a 5-axis tool changer, including hardware, configuration, calibration, and more (release imminent)
#     - toolpath design directly in FullControl
#         - preliminary version already included in the 'FullControl lab' - see the example below, and the [5-axis demo notebook](lab_five_axis_demo.ipynb)
# - multi-tool
# - multi-hardware
# - geometry import and interrogation (STL and similar)
# - in-process inspection and correction
# - upload of models to www.fullcontrol.xyz
#     - if you're able and interested in turning www.fullcontrol.xyz into the ***best website ever*** for additive manufacturing, please get in touch: [info@fullcontrol.xyz](mailto:info@fullcontrol.xyz)
# 
# additional functionality beyond that listed above is planned for ongoing research by Andy Gleadall, which will also be made open-source whenever possible
# 
# please improve FullControl and add capabilities to it
# - e.g. to support journal papers that present new methods for additive manufacturing by making those methods available to everyone via FullControl

# #### five_axis example
# 
# this example shows a wavey helical print path, where the model is continuously rotating while the nozzle gradually moves away from the print platform
# 
# the part is tilted to orient the nozzle perpendicular(ish) to the wavey walls at all points
# 
# color data is added to visualize the b axis

# In[ ]:


import lab.fullcontrol.fiveaxis as fc5
from math import sin, cos, tau
steps = []
for i in range(10001):
    angle = tau*i/200
    offset = (1.5*(i/10000)**2)*cos(angle*6)
    steps.append(fc5.Point(x=(6+offset)*sin(angle), y=(6+offset)*cos(angle), z=((i/200)*0.1)-offset/2, b=(offset/1.5)*30, c=angle*360/tau))
for step in steps:
    if type(step).__name__ == 'Point':
        # color is a gradient from B=0 (blue) to B=45 (red)
        step.color = [((step.b+30)/60), 0, 1-((step.b+30)/60)]
steps.append(fc5.PlotAnnotation(point=fc5.Point(x=0, y=0, z=8.75), label='color indicates B axis (tilt)'))
steps.append(fc5.PlotAnnotation(point=fc5.Point(x=0, y=0, z=7.5), label='-30 deg (blue) to +30 deg (red)'))
gcode = fc5.transform(steps,'gcode')
print('final ten gcode lines:\n' + '\n'.join(gcode.split('\n')[-10:]))
fc5.transform(steps, 'plot', fc5.PlotControls(color_type='manual', hide_axes=False, zoom=0.75, style='line'))

#!/usr/bin/env python
# coding: utf-8

# # PlotControls adjust how a ***design*** is transformed into a 'plot' ***result***
# 
# ***designs*** are transformed into a 'plot' according to some default settings which can be overwritten with a PlotControls object with the following attributes (all demonstrated in this notebook):
# 
# - `color_type` - options: 'random_blue', 'z_gradient', 'print_sequence', 'print_sequence_fluctuating', 'manual'
# - `zoom` - recommended range 0.1 - 10
# - `hide_annotations` - True/False
# - `hide_travel` - True/False
# - `hide_axes` - True/False
# - `neat_for_publishing` - True/False (square format for consistent png creation)
# - `raw_data` - True/False (output data instead of creating a plot)
# - `style` - options: 'tube'/'line' - preview 3D real-printed-volume lines or simple lines with non-representative widths
#     - if `style == 'tube'`:
#         - `tube_type` - options: 'flow'/'cylinders' - adjust how the plot transitions from line to line
#         - `tube_sides` - sides of the prisms created for the 3D real-printed-volume lines
#         - `initialization_data` - define initial width/height of 3D lines with dictionary: {'extrusion_width': value, 'extrusion_height': value}
#     - if `style == 'line'`:
#         - `line_width` - recommended range 0.1 - 10
#     
# custom plots can be created with the raw data as demonstrated below
# 
# <*this document is a jupyter notebook - if they're new to you, check out how they work:
# [link](https://www.google.com/search?q=ipynb+tutorial),
# [link](https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb),
# [link](https://colab.research.google.com/)*>
# 
# *run all cells in this notebook in order (keep pressing shift+enter)*

# In[ ]:


import fullcontrol as fc

# this demo design is used for most of the plots in this notebook
centre_point = fc.Point(x=50, y=50, z=0)
steps = fc.helixZ(centre_point, 20, 15, 0, 30, 0.15, 30*64)
steps.append(fc.Extruder(on=False))
steps.append(fc.PlotAnnotation(label='extruder off'))
steps.append(fc.Point(x=50, y=50, z=0))
steps.append(fc.Extruder(on=True))
steps.append(fc.PlotAnnotation(label='extruder on'))
steps.append(fc.Point(z=5))
steps.append(fc.PlotAnnotation(label='finish'))
steps.append(fc.PlotAnnotation(point=steps[0], label='start'))


# #### default plot style
# 
# lines are shown as 3D lines, where width and height are defined by the extrusion width and height set in initialization data or through ExtrusionGeometry objects in the ***design*** - if unset, default values are width 0.4 and height 0.2

# In[ ]:


fc.transform(steps, 'plot')


# #### change color and hide axes / annotations / travel

# In[ ]:


plot_controls = fc.PlotControls(line_width=4, color_type='print_sequence', hide_axes=True, hide_annotations=True, hide_travel=True)
fc.transform(steps, 'plot', plot_controls)


# #### 'neat_for_publishing' and 'zoom'
# 
# create a square plot for consistent generation of images for publication with neat_for_publishing=True
# 
# hover the mouse over the plot and click the camera button ("Download plot and png")
# 
# 'zoom' is used to set the initaial zoom level of the plot

# In[ ]:


fc.transform(steps, 'plot', fc.PlotControls(neat_for_publishing=True, zoom=0.6))


# #### change line size
# 
# extrusion width and height are controlled in the ***design*** with ExtrusionGeometry objects, as discussed in the State Objects notebook
# 
# these objects are automatically evaluated - they dictate the widths and heights of lines in the plot
# 
# the plot can be initated with specific widths and heights by including an 'initialization_data' dictionary in PlotControls (first example below)
# 
# the specified width and height remain throughout the plot unless the design includes ExtrusionGeometry objects (second example below)
# 
# if no intitialization data is provided, default values are used: 0.4 wide x 0.2 high

# In[ ]:


plot_controls = fc.PlotControls(initialization_data={'extrusion_width': 0.1, 'extrusion_height': 0.1})
fc.transform(steps, 'plot', plot_controls)


# #### 'tube_type'
# 
# set to 'flow' to get smooth transitions between linear segments of the path - this leads to much neater visuals for curves and allows gradual transitions when extrusion width is changed
# 
# set to 'cylinders' to get a more strict preview of widths defined in the ***design*** - each tube has a contant width according to the designed width

# In[ ]:


varying_width_steps = []
varying_width_steps.append(fc.Point(x=0, y=5, z=0.1)) # start point (width defaults to 0.4)
varying_width_steps.append(fc.ExtrusionGeometry(width=0.6, height=0.4))
varying_width_steps.append(fc.Point(y=0)) # print to this point with width 0.6
varying_width_steps.append(fc.ExtrusionGeometry(width=1))
varying_width_steps.append(fc.Point(x=5)) # print to this point with width 1
varying_width_steps.append(fc.ExtrusionGeometry(width=1.5))
varying_width_steps.append(fc.Point(y=5)) # print to this point with width 1.5
fc.transform(varying_width_steps + [fc.PlotAnnotation(label='tube_type="flow" (view from above to see clearly)')], 'plot', fc.PlotControls(color_type='print_sequence', tube_type="flow")) # default tube_type="flow"
fc.transform(varying_width_steps + [fc.PlotAnnotation(label='tube_type="cylinders" (view from above to see clearly)')], 'plot', fc.PlotControls(color_type='print_sequence', tube_type="cylinders"))


# #### manual colors
# 
# set color_type='manual' and assign [r, g, b] colors to points for manual colors
# 
# any points without the attribute 'color' defined will inherit the color of the previous point
# 
# colors automatically transition over the length of a line between points with different colors

# In[ ]:


colored_steps = []
colored_steps.append(fc.Point(x=0, y=0, z=0.2, color=[1, 0, 0]))
colored_steps.append(fc.Point(x=40, y=4, color=[1, 0.8, 0]))
colored_steps.append(fc.Point(x=0, y=8))
fc.transform(colored_steps, 'plot', fc.PlotControls(color_type='manual'))


# #### 'tube_sides'
# 
# extuded lines are plotted as 6-sided hexagonal prisms by default, but the number of sides can be change

# In[ ]:


steps_line = [fc.Point(x=0, y=0, z=0.1), fc.Point(y=1), fc.Point(y=2)]
fc.transform(steps_line + [fc.PlotAnnotation(label='8-sided tube', point=steps_line[0])], 'plot', fc.PlotControls(color_type='print_sequence', style="tube", tube_sides=8))


# #### plot_style (line)
# 
# as opposed to plotting the path as 3D lines with real volumes representing the width and height of extruded lines, it is possible to create a simple line plot
# 
# zooming in and out of a line plot does not change the line size and it does not represent the width or height of printed lines
# 
# the width of the line can be controlled with the 'line_width' attribute
# 
# however, this type of plot has the advantage that it is less computationally demanding, which may be important for larger models
# 
# also, this plot is useful for design since the mouse cursor can be used to identify coordinates of points directly on the print path (nozzle position) as opposed to identiying points on the surface of the 3D line preview (tublular structures)

# In[ ]:


fc.transform(steps + [fc.PlotAnnotation(point=fc.Point(x=50, y=50, z=15), label='zoom in to see line width remain constant')], 'plot', fc.PlotControls(style='line', line_width=2))


# #### output and inspect raw data

# In[ ]:


plot_controls = fc.PlotControls(raw_data=True)
plot_data = fc.transform(steps, 'plot', plot_controls)
print('first five values of the first path:')
print(f'    x values: {plot_data.paths[0].xvals[0:4]}')
print(f'    y values: {plot_data.paths[0].yvals[0:4]}')
print(f'    z values: {plot_data.paths[0].zvals[0:4]}')
print(f'    extrusion width values: {plot_data.paths[0].widths[0:4]}')
print(f'    extrusion height values: {plot_data.paths[0].heights[0:4]}')
print(f'    color values [r, g, b]: {plot_data.paths[0].colors[0:4]}')
print(f'    extruder state: {plot_data.paths[0].extruder.on}')
print(f'second path (travel line of two points):\n    {plot_data.paths[1]}')
print(f'final path (vertical line of two points):\n    {plot_data.paths[2]}')
print(f'plot_data.annotations:\n    {plot_data.annotations}')
print(f'plot_data.bounding_box:\n    {plot_data.bounding_box}')


# #### create custom plots
# 
# this is the same path as in previous plots but this plot doesn't scale xyz axes equally

# In[ ]:


def custom_plot(data):
    import plotly.graph_objects as go
    fig = go.Figure(layout=go.Layout(template='plotly_dark'))
    for i in range(len(data.paths)):
        line_color = 'rgb(255,160,0)' if data.paths[i].extruder.on == True else 'rgb(200,0,0)'
        fig.add_trace(go.Scatter3d(mode='lines', x=data.paths[i].xvals, y=data.paths[i].yvals,z=data.paths[i].zvals, line=dict(color=line_color)))
    import plotly.io as pio
    from datetime import datetime
    pio.write_image(fig, datetime.now().strftime("figure__%d-%m-%Y__%H-%M-%S.png"))
    
plot_controls = fc.PlotControls(raw_data=True)
plot_data = fc.transform(steps, 'plot', plot_controls)
custom_plot(plot_data)

#!/usr/bin/env python
# coding: utf-8

# # objects for changing ***state***
# 
# the pre-defined templates for objects in a FullControl ***design***, which describes changes to ***state***, are demonstrated here
# 
# after creating a FullControl ***design***, it is transformed into a ***result*** (e.g. gcode or a 3D plot preview). this notebook is focused on ***designs*** that are transformed into 'gcode' or 'plot' ***results*** - both types are already built into FullControl and have default settings. gcode can be formatted for a selection of printers and the 3D plot is implemented in plotly, but the range of printers is intended to be extended along with plotting software options 
# 
# more details of the transformation methods are given in separate notebooks ([gcode](gcode_controls.ipynb), [plot](plot_controls.ipynb))
# 
# some changes to ***state*** affect both ***results*** (e.g. x y z values of Points); some only affect the 'plot' ***result*** (e.g. color of Points); some only affect the 'gcode' ***result*** (e.g. fan speed).
# 
# when the design is being transformed into a gcode ***result***, design intentions that cannot be expressed by existing templates for ***state***-change objects can be defined using a ManualGcode object. information about adding new templates will be described in future documentation aimed at python developers
# 
# <*this document is a jupyter notebook - if they're new to you, check out how they work:
# [link](https://www.google.com/search?q=ipynb+tutorial),
# [link](https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb),
# [link](https://colab.research.google.com/)*>
# 
# *run all cells in this notebook in order (keep pressing shift+enter)*

# In[ ]:


import fullcontrol as fc


# # 1. generic objects
# 
# the objects in this section are not specific to one ***result***-type, they may influence multiple different ***results***

# ## Point
# 
# Point classes describe where the printhead should move to with x y z attributes

# In[ ]:


steps = []
steps.append(fc.Point(x=0,y=0,z=0))
steps.append(fc.Point(x=10,y=0,z=0))
steps.append(fc.Point(x=10,y=10,z=0))
print(fc.transform(steps, 'gcode'))


# it is not necessary to define x, y and z - you can define only the coordinates that change - but the first point should have all of x y and z defined

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.Point(x=10))
steps.append(fc.Point(y=10))
print(fc.transform(steps, 'gcode'))


# the color attribute of points can be defined for a 'plot' ***result*** 
# 
# color is described by a list [r, g, b] with values from 0 to 1

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0, color=[0,0,1]))
steps.append(fc.Point(x=50, y=5, color=[0,1,1]))
steps.append(fc.Point(x=0, y=10, color=[1,0,1]))
fc.transform(steps, 'plot', fc.PlotControls(color_type='manual'))


# similar to the x y z point attributes, you only need to define the color attribute if it changes
# 
# to get an instant change in color, as opposed to a transition between two points, add a Point object with no change to x y z but a change to color

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0, color=[0,0,1]))
steps.append(fc.Point(x=25, y=5))
steps.append(fc.Point(x=0,y=10))
steps.append(fc.Point(y=30, color=[0,1,1])) # line plotted with a gradient transition to this color
steps.append(fc.Point(x=25, y=40))
steps.append(fc.Point(x=0, y=50))
steps.append(fc.Point(color=[0,0,1])) # line plotted with an instant color change
steps.append(fc.Point(y=60))
fc.transform(steps, 'plot', fc.PlotControls(color_type='manual'))


# ## Fan
# 
# speed is set as a percent, which is converted to the range 0-255 in gcode

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.Point(x=5))
steps.append(fc.Fan(speed_percent=50))
steps.append(fc.Point(x=10))
steps.append(fc.Fan(speed_percent=0))
print(fc.transform(steps, 'gcode'))


# ## Buildplate
# 
# the temperature of the buildplate can be set along with an instruction as to whether the printer should wait for the desired temperature to be reached before continuing

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.Point(x=5))
steps.append(fc.Buildplate(temp=80, wait=False))
steps.append(fc.Point(x=10))
steps.append(fc.Buildplate(temp=80, wait=True))
print(fc.transform(steps, 'gcode'))


# ## Hotend
# 
# the temperature of the hotend is set along with an instruction to say whether the printer should wait for the desired temperature to be reached before continuing
# 
# the tool can also be stated for multitool printers

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.Point(x=5))
steps.append(fc.Hotend(temp=280, wait=True))
steps.append(fc.Point(x=10))
steps.append(fc.Hotend(temp=170, wait=False, tool=3))
print(fc.transform(steps, 'gcode'))


# ## Printer
# 
# used to set print speed and travel speed (for non-extruding movements)

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.Point(x=5))
steps.append(fc.Point(x=10))
steps.append(fc.Printer(print_speed=500, travel_speed=2000))
steps.append(fc.Point(x=15))
steps.append(fc.Point(x=20))
steps.append(fc.GcodeComment(text="'F500' is not included in the gcode line immediately above since the printer remembers it from the previous line"))
print(fc.transform(steps, 'gcode'))


# ## ExtrusionGeometry
# 
# set the geometry of the extruded material, which is used to calculate the value of E in gcode
# 
# the 'area_model' attribute controls how the cross-sectional area of the extrudate is defined. it can be set to 'rectangle' (default), 'stadium', 'circle' or 'manual'
# 
# a 'stadium' is a rectangle with a semi-circle at each end
# 
# if 'area_model' == 'rectangle' or 'stadium', width and height must be defined
# 
# in some cases, cylindrical extrudates are expected, in which case area_model='circle' is logical and diameter must be defined
# 
# to manually set the cross-sectional, set area_model='manual' and set the 'area' attribute as desired

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.ExtrusionGeometry(area_model='rectangle', width=0.8, height=0.2))
steps.append(fc.Point(x=10))
steps.append(fc.ExtrusionGeometry(width=0.4))
steps.append(fc.Point(x=20))
print(fc.transform(steps, 'gcode'))


# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.Extruder(units='mm3'))  # set extrusion units to mm3 to make it easier to manually calculate E values
steps.append(fc.ExtrusionGeometry(area_model='rectangle', width = 1, height = 0.2))
steps.append(fc.Point(x=1))
steps.append(fc.GcodeComment(end_of_previous_line_text='     E = length (1 mm) * width (1 mm) * height (0.2 mm) = 0.2 mm3'))
steps.append(fc.ExtrusionGeometry(width=0.5))
steps.append(fc.Point(x=2))
steps.append(fc.GcodeComment(end_of_previous_line_text='     width halved, but length and height remained the same, so E halved'))
steps.append(fc.ExtrusionGeometry(area_model='circle', diameter=1))
steps.append(fc.Point(z=10))
steps.append(fc.GcodeComment(end_of_previous_line_text='     print a z-pillar. area_model = circle. E = length (10 mm) * pi (3.14) * (d^2)/4 (1*1/4=0.25) = 7.85 mm3'))
steps.append(fc.ExtrusionGeometry(area_model='manual', area=2))
steps.append(fc.Point(z=20))
steps.append(fc.GcodeComment(end_of_previous_line_text='     area_model = manual. E = length (10 mm) * area (2 mm2) = 20 mm3'))
print(fc.transform(steps, 'gcode'))


# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0.5))
steps.extend([fc.ExtrusionGeometry(width=1, height=0.5), fc.PlotAnnotation(label='W1 H0.5'), fc.Point(x=5)])
steps.extend(fc.travel_to(fc.Point(x=0, y=-2)))
steps.extend([fc.ExtrusionGeometry(area_model = 'circle', diameter = 0.5), fc.PlotAnnotation(label='Circle dia 0.5'), fc.Point(x=5)])
steps.extend(fc.travel_to(fc.Point(x=0, y=-4)))
steps.extend([fc.ExtrusionGeometry(area_model = 'circle', diameter = 1), fc.PlotAnnotation(label='Circle dia 1'), fc.Point(x=5)])
steps.extend(fc.travel_to(fc.Point(x=0, y=-6)))
steps.extend([fc.ExtrusionGeometry(area_model = 'manual', area = 0.5), fc.PlotAnnotation(label='Manual area 0.5'), fc.Point(x=5)])
steps.extend(fc.travel_to(fc.Point(x=0, y=-8)))
steps.extend([fc.ExtrusionGeometry(area_model = 'manual', area = 1), fc.PlotAnnotation(label='Manual area 1'), fc.Point(x=5)])
fc.transform(steps, 'plot', fc.PlotControls(style="tube", color_type='print_sequence', tube_type='cylinders', tube_sides=8))


# ## Extruder
# 
# the 'on' attribute of an Extruder object is used to turn extrusion on or off - it defaults to True if not set

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0.2))
steps.append(fc.Point(x=25))
steps.append(fc.Extruder(on=False))
steps.append(fc.Point(x=0, y=5))
steps.append(fc.Extruder(on=True))
steps.append(fc.Point(x=25))
fc.transform(steps, 'plot')


# other potential attributes of an Extruder are
# - 'units': units of E in gcode ('mm' or 'mm3')
# - 'dia_feed': diameter of the feedstock filament (mm)
# - 'relative_gcode': E values in gcode are relative (see 'M83' in general gcode documentation) if set to True

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.Point(x=5))
steps.append(fc.Point(x=10))
steps.append(fc.Extruder(dia_feed=2.85))
steps.append(fc.GcodeComment(text='dia_feed changed from default 1.75 to 2.85 mm: E value changes'))
steps.append(fc.Point(x=15))
steps.append(fc.Point(x=20))
steps.append(fc.Extruder(units='mm3'))
steps.append(fc.GcodeComment(text='units changed from default mm to mm3: E value changes'))
steps.append(fc.Point(x=25))
steps.append(fc.Point(x=30))
steps.append(fc.Extruder(relative_gcode=False))
steps.append(fc.GcodeComment(text='relative_gcode changed from default True to False: E value increases incrementally'))
steps.append(fc.Point(x=35))
steps.append(fc.Point(x=40))
steps.append(fc.Point(x=45))
steps.append(fc.Point(x=50))
print(fc.transform(steps, 'gcode'))


# ## StationaryExtrusion
# 
# extrude material from the nozzle without moving in XYZ
# 
# volume is defined in mm^3
# - note the number for E in gcode will not be equal to volume for most printers - but FullControl does the unit conversion for you
# 
# speed is dependent on your printer but will most likely be
# - *units_of_E_for_your_printer* / minute
# 

# In[ ]:


steps = []
steps.append(fc.Extruder(on=False))
steps.append(fc.Extruder(units='mm3'))
steps.append(fc.Point(x=10, y=10, z=2))
steps.append(fc.StationaryExtrusion(volume=5, speed=50))
steps.append(fc.Point(x=20, y=10, z=2))
steps.append(fc.StationaryExtrusion(volume=5, speed=100))
print(fc.transform(steps, 'gcode'))


# ## PrinterCommand
# 
# to allow FullControl ***designs*** to create 'gcode' ***results*** for various printers, each printer has a list of commands that can be called to change ***state***
# 
# a few demo commands are automatically included for each Printer. the most likely to be used during design are:
# - "retract" = "G10 ; retract"
# - "unretract" = "G11 ; unretract"
# 
# each command has an 'id' which can be memorable and easy to include in a ***design*** than a ManualGcode object
# 
# to call a command, the PrinterCommand object is used

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.Point(x=10))
steps.append(fc.Extruder(on=False))
steps.append(fc.PrinterCommand(id='retract'))
steps.append(fc.Point(x=0, y=2))
steps.append(fc.Extruder(on=True))
steps.append(fc.PrinterCommand(id='unretract'))
steps.append(fc.Point(x=10))
print(fc.transform(steps, 'gcode'))


# new commands can be added using the extend_commandlist attribute of a Printer object
# 
# information about changing the command list permanently will be provided in future documentation about adding new printers

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.Printer(new_command={'pause': 'M601 ; pause print'}))
steps.append(fc.Point(x=10))
steps.append(fc.PrinterCommand(id='pause'))
steps.append(fc.Point(x=20))
steps.append(fc.PrinterCommand(id='pause'))
steps.append(fc.Point(x=30))
steps.append(fc.PrinterCommand(id='pause'))
print(fc.transform(steps, 'gcode'))


# # 2. ***result***-specific objects
# 
# the objects in this section target a specific ***result***
# 
# this is done for convenience but could change in the future. E.g. an alternative approach for 'GcodeComment' and 'PlotAnnotation' (both described below) would be to have a single 'annotation' object that applies a comment to gcode and written text to a plot, but that approach isn't implemented in this release to allow the objects to be more easily tailored to the specific type of ***target***
# 
# the objects that target the 'plot' ***result*** are ignored when the ***design*** is transformed to a 'gcode' ***result*** and vice versa

# ## GcodeComment
# 
# a comment can be added to the gcode as a new line or as an addition to the previous line of gcode

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.GcodeComment(text='comment as a new line of gcode'))
steps.append(fc.Point(x=10))
steps.append(fc.GcodeComment(end_of_previous_line_text='comment added to the end of the previous line of gcode'))
print(fc.transform(steps, 'gcode'))


# ## ManualGCode
# 
# if design intentions cannot be expressed by the above objects to control ***state***, the ManualGcode object can be used to insert gcode at any point in the ***design***
# 
# CAUTION: this is a bit of a hack... any changes to state implemented by manual gcode will not be tracked by FullControl when converting the ***design*** to a ***result*** (for both types - gcode and plot). 
# - e.g. if manual gcode "G1 X0" was added, the ***state*** of the printer would not be updated by this command. Therefore the next line of gcode would potentially have an incorrect length calculated and, therefore, an incorrect E-value calculated. Similarly, the lines in a 'plot' ***result*** would not include the X0 position.
# - e.g. if manual gcode "G91; relative positioning" was added, FullControl would still output absolute x y z values for all subsequent Points

# In[ ]:


steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.ManualGcode(text="G4 P2000 ; pause for 2 seconds"))
steps.append(fc.Point(x=10))
print(fc.transform(steps, 'gcode'))


# ## PlotAnnotation
# 
# annotations can be added to plots
# 
# if the 'point' attribute is not supplied, the annotation appears at the current position of the printer when the annotation appears in the ***design*** (list of steps)
# 
# if the 'point' attribute is supplied, this is used to dictate the position of the annotation and means that it doesn't matter where they are defined in the list of steps

# In[ ]:


steps = []
steps.append(fc.Point(x=20, y=10, z=0.2))
steps.append(fc.PlotAnnotation(label="start point"))
steps.append(fc.Point(x=30, y=20))
steps.append(fc.Point(x=20, y=30))
steps.append(fc.Point(x=10, y=20))
steps.append(fc.PlotAnnotation(label="end point"))
fc.transform(steps, 'plot')


# In[ ]:


steps = []
steps.append(fc.Point(x=20, y=10, z=0.2))
steps.append(fc.Point(x=30, y=20))
steps.append(fc.Point(x=20, y=30))
steps.append(fc.Point(x=10, y=20))
steps.append(fc.PlotAnnotation(label="centre point", point=fc.Point(x=20, y=20, z=0)))
steps.append(fc.PlotAnnotation(label="3 mm above the bed", point=fc.Point(x=20, y=20, z=3)))
fc.transform(steps, 'plot')

