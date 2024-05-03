# roadmap:

sooner:
- release python version of models on [fullcontrol website](https://fullcontrol.xyz)
- export 3D mesh of model
    - stl using [VOLCO](https://doi.org/10.1016/j.addma.2018.04.004)
- real time control
- add tutorial info about path length function, circleXY_3pt, catmull_rom, bezier_through_points, interpolated_point, segmented_path
- warn user if they set `line_width` in PlotControls but `style` is not set to 'line' (default = 'tube')
- expose calc_bounds() to users
- migrate to pydantic >2.0 - ensure all requirements are met by colab without any dependent package uninstall+reinstall if possible
- investigate: does fc.Point(color= ???) break when calculating colour if not manual colour? What if this is the first point in the list of steps?
- checks to implement before transform()
    - first point in steps has a z value? is this required for sure?
    - first point has color value (if color specified anywhere?) or if color_type = 'manual' in PlotControls
- add checks for common mistakes (e.g. list included in 'steps'; first point not fully defined; decorator to check xy or xyz values set for all points for certain geometric functions)
- make travel_to work with lists (copy relevant code from extra_functions.first_point())
- release new version (changed docstrings and repo structure), modify installation instructions + notebooks to use pip install fullcontrol instead of git+https://github.com/FullControlXYZ/fullcontrol - and update version on pypi
- update main readme to say users can install from pypi (latest official release) or from github (git+...) to the most up to date version or clone the repo.
- add instructions for cicd testing - clarify how the user can ensure tests are completed using the correct version of fullcontrol (temporatily place scripts in the root directory and run there?). explain that any updates to tutorials will mean tutorial_to_py.py will need to be run again.
- create a maths/geometry onboarding-to-expert tutorial (at expert end of the scale, put some prompts about what-ifs for things like switching from CAD to maths or using chatGPT) - "from beginning to expert in 15 minutes!"
    - spend a few minutes learning basics of polar angles, sin waves, etc. then show how they compound into amazing complex geometry using good prompts in chatGPT (but there needs to be a reliable maths chatGPT)
- In extrusion_classes.py; line 79; potential change to avoid "E5.6e-5"?
    - return f'E{round(self.get_and_update_volume(length*state.extrusion_geometry.area)*self.volume_to_e, 6)} '
    - to
    - return f'E{round(self.get_and_update_volume(length*state.extrusion_geometry.area)*self.volume_to_e, 6):.6f} '
- create new meta repo for fullcontrol_profile_integration
    - rename the json variables to be my own terms (start_gcode instead of machine_start_gcode) so that all the other data soruces can translate into the same FC format
    - one directory in that will be for cura
        - only include a script (or description) of which commit to pull and the git command to do that, full-variable folder, filtered-variable json folder (these will go into fc), and bin folder
    - explain how to import and printer in fc
        - show how to edit the imported printer profile (edit parameters, or edit line X of start_gcode)
        - allow users the option to supply tranform function with a printer_data object as opposed to a string id.
- add 'devices' directory to fullcontrol repo (devices.[VENDOR].[MANUFACTURER_MODEL.json]) /w enum,selection api
    - cura is in here as well as fullcontrol (original printers?) and community? (for people to add printers too?) ... not quite logical... community and fullcontrol are the same thing atm.


later:
- refactor documentation - [issue](https://github.com/FullControlXYZ/fullcontrol/issues/10)
- update website (www.fullcontrol.xyz) to have more information and have normal website sections? Release website code as open-source repo.
- generalised multi-axis capabilities
- 6-axis robots
- simultaneous control of distributed devices
- collision detection (nozzle/printer-frame/printed-object) - [issue](https://github.com/FullControlXYZ/fullcontrol/issues/21)
- rounded squarewave - [issue](https://github.com/FullControlXYZ/fullcontrol/issues/34)
- show print bed in preview - [issue](https://github.com/FullControlXYZ/fullcontrol/issues/9)
- facilitate 2D plotters (variable line width) - [issue](https://github.com/FullControlXYZ/fullcontrol/issues/15)
- facilitate easy SVG import - [issue](https://github.com/FullControlXYZ/fullcontrol/issues/11)
- allow use of more complex gcode commands like G2/G3 - [issue](https://github.com/FullControlXYZ/fullcontrol/issues/2)
- warn user if centre point has no z value defined - [issue](https://github.com/FullControlXYZ/fullcontrol/issues/36)
- cell control (e.g. dual robots; e.g. printer with supplemental hardware that is not part of the printer)
- area control (e.g. printer farms with microcontrollers)
- factory control (e.g. production line(s))
- enterprise control (e.g. multiple factories)