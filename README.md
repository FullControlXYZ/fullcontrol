# FullControl

## intro

the conventional method to generate gcode is: create cad model -> export stl -> slice into layers -> create paths for each layer -> output path as gcode

FullControl offers a different approach where the print path is explicitly designed. imagine being given a hotmelt glue-gun and told to move it around to 'print' layers resulting in a 30-mm cube. you could design lots of different paths that would achieve the cube. FullControl allows you to design and preview print paths and convert them to machine-code instructions for a 3D printer (a gcode file)

the overall printing procedure may be considered to be predominantly a stream of points. then a few extra things are sprinkled in occasionally, like changes to speed, temperature, fans, etc. 

all of these things together (points and the extra things) are referred to as ***state*** in FullControl. ***state*** is basically any property of interest that can change

FullControl allows designs to be created that control changes the ***state*** of ***things***, where ***things*** are anything with ***state*** - this initial release of FullControl is focused on the ***thing*** being an extrusion 3D printer that is instructed by gcode. however, ***things*** really could be anything (laser cutters, assembly lines, non-physical things like a 3D visualization, etc.)


## FullControl history

"FullControl gcode designer" (2020) ([website](http://www.fullcontrolgcode.com), [github](https://github.com/AndyGlx/FullControl-GCode-Designer), [journal paper](https://www.researchgate.net/publication/352732664))
- users generate gcode by directly designing geometric 'features' and custom gcode 'features'
- microsoft excel used as the user interface for design creation. FullControl algorithms written in visual basic. gcode previewed in other software (e.g. repetier host)
- targeted researchers and people experimenting with printers and other gcode-based hardware, who need to explicitly design print paths with 'full control'

"www.fullcontrol.xyz" (2022):
- users generate and download gcode parametrically for pre-created designs directly from a [website](https://fullcontrol.xyz)
- no need for experience of printing, gcode, CAD, toolpath design, python, etc.
- demo models created with the python implementation of FullControl (i.e. this repository)

"FullControl" (2023) - this repository:
- users design, preview, and export gcode for custom print paths for extrusion 3D printing, all in a python environment
- 'designs' are python scripts or jupyter notebooks
- the initial release (March 2023) is a gcode-focused implementation of the broader FullControl concept to design changes to the ***state*** of ***things***

## using FullControl

jupyter notebooks are provided in the [docs](https://github.com/FullControlXYZ/fullcontrol/tree/master/docs) folder of this github repository (repo) to introduce FullControl and demonstrate its use

a future update of this repo will give more details about the python code

## installation

```
pip install git+https://github.com/FullControlXYZ/fullcontrol
```

alternatively clone this git repo and run "pip install ." from the repo directory

## use

to use FullControl, create a python script or jupyter notebook and import the fullcontrol package

```
import fullcontrol as fc
```

## structure of the repository

the FullControl repository is organized as follows:

* `docs`: jupyter notebooks describing FullControl and its use. For more details, check the readme [here](https://github.com/FullControlXYZ/fullcontrol/tree/master/docs) or jump straight in to the [1-minute demo](https://githubtocolab.com/FullControlXYZ/fullcontrol/blob/master/docs/colab/fast_demo_colab.ipynb)
* `fullcontrol`: the FullControl python package. For more details, check the readme [here](https://github.com/FullControlXYZ/fullcontrol/tree/master/fullcontrol)
* `lab`: the FullControl lab python package for experimental features. For more details, check the readme [here](https://github.com/FullControlXYZ/fullcontrol/tree/master/lab)
* `bin`: scripts for FullControl development activities

## feedback

please use the github [issues](https://github.com/FullControlXYZ/fullcontrol/issues) tab for this repository to give feedback.

## pull requests

please submit pull requests for bugfixes, optimizations, documentation corrections/clarifications, etc., and for minor additions and new features such as functions, objects, and modules that fit into the existing package structure

for revisions that change the structure, behaviour, or usage of the software, please email us ([info@fullcontrol.xyz](mailto:info@fullcontrol.xyz)) prior to submitting a pull request. this is to ensure alignment between the changes and any planned/unpublished revisions already in progress. note that this version of FullControl is not targeted at developers - the structure of the repo may change and more information about the code structure will be provided at a later date to accommodate contribution more readily

note that the docs folder of this repo contains tutorial notebooks. executing cells in these notebooks leads to timestamp changes, even if the cell content remains unchanged. this may cause unexpected issues and complications for pull requests. until a more automated solution is implemented, consider two options before submitting a pull request:
1. create a fresh clone of the FullControl repo and copy the relevant changes across (recommended)
1. use the git stash operation on the docs folder (be careful not to unintentionally stash any of your proper changes though)

## license
FullControl is released under the [GPL v3 License](https://github.com/FullControlXYZ/fullcontrol/blob/master/LICENSE).

## copyright

FullControl, FullControlXYZ, copyright 2023 Andrew Gleadall and Dirk Leas

## references

until the journal paper for FullControl is available, please cite the paper for 'FullControl GCode Designer':

```
Gleadall, A. (2021). FullControl GCode Designer: open-source software for unconstrained design in additive manufacturing. Additive Manufacturing, 46, 102109.
```

## contact
 - [info@fullcontrol.xyz](mailto:info@fullcontrol.xyz)
 - individual emails:
    - Andy Gleadall - andy@fullcontrol.xyz
    - Dirk Leas - dirk@fullcontrol.xyz
