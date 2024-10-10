# roadmap:

sooner:
- release python version of models on [fullcontrol website](https://fullcontrol.xyz)
- export 3D mesh of model
    - stl using [VOLCO](https://doi.org/10.1016/j.addma.2018.04.004)
- real time control
- add tutorial info about path length function, circleXY_3pt, catmull_rom, bezier_through_points, interpolated_point, segmented_path
- release new version (changed docstrings and repo structure), modify installation instructions + notebooks to use pip install fullcontrol instead of git+https://github.com/FullControlXYZ/fullcontrol - and update version on pypi
- update main readme to say users can install from pypi (latest official release) or from github (git+...) to the most up to date version or clone the repo.

- create 'projects' on github to bring together work relevant to multiple 'issues'

- create a maths/geometry onboarding-to-expert tutorial (at expert end of the scale, put some prompts about what-ifs for things like switching from CAD to maths or using chatGPT) - "from beginning to expert in 15 minutes!"
    - spend a few minutes learning basics of polar angles, sin waves, etc. then show how they compound into amazing complex geometry using good prompts in chatGPT (but there needs to be a reliable maths chatGPT)

- add docs explaining how to import and printer in fc from Cura/ and Community/
    - show how to edit the imported printer profile (edit parameters, or edit line X of start_gcode)
    - explain how to find printer names (link to github list or add a search function)
- consider moving 'devices' directory to top level fullcontrol repo (devices.[VENDOR].[MANUFACTURER_MODEL.json]) /w enum,selection api (not done at present becuase cura manufacturer and model data are inconsistent)

- add docs to explain options for heavy use: e.g. massive simulations on a virtual CPU/GPU
- make a create_rag() function that combines a few of the tutorial notebooks, maybe geometry functions and maybe some additional prompts into a single file like a PDF.

- create new meta repo for fullcontrol_profile_integration
    - one directory in that will be for cura
        - include script to extract printer profiles from cura library and state which commit of the cura repo to pull and the git command to do that, full-variable folder, filtered-variable json folder, minimal variable folder (duplicated in main fc repo), and bin folder

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