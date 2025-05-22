# FullControl LLM Reference Document

## Introduction
- Purpose of this document: To provide a comprehensive reference for the FullControl repository, explaining its architecture, components, and usage patterns.
- Files examined to create the document: Core modules, geometry functions, visualization modules, G-code generation modules, lab features, and tutorials (particularly overview.ipynb).
- Limitations and update notes: This document is based on the current state of the repository and may need updates as the library evolves.
- Key coding patterns: The library uses a state-based approach where a design is a list of steps that change the state of a 3D printer, which is then transformed into either G-code or visualization. All objects in the steps list must be FullControl objects with implemented `gcode()` and `visualize()` methods.
- Core concept: FullControl is fundamentally about designing changes to the "state" of "things", where "state" is any property that can change (position, speed, temperature, etc.) and "things" are anything with state (primarily 3D printers in the current implementation, but the concept can be extended to many other domains as explained in section 1.2).

## 1. Repository Overview

### 1.1 Primary Focus: 3D Printing
- FullControl is a Python library primarily focused on designing 3D printing paths with precise control over printer movements and states.
- The library transforms a design (a list of steps that change the state of a 3D printer) into a result (G-code or visualization).
- The main philosophy is to give users full control over the printing process by allowing them to define exact movements and state changes.
- The library is designed to be extensible, with a core set of functionality and experimental features in the lab module.
- FullControl allows for precise control over every aspect of the printing process, unlike conventional slicing software that makes many decisions automatically.
- While the repository contains mostly 3D printing examples, it also includes examples for laser cutting, demonstrating the flexibility of the approach.

### 1.2 Broader Applications: Beyond 3D Printing
- The core concept of FullControl—designing changes to the "state" of "things"—can be applied to many domains beyond 3D printing:
  - **Drone Path Planning**: Defining precise flight paths, speeds, and actions for drones, with states including position, orientation, altitude, and payload operations.
  - **CNC Machining**: Controlling tool paths, cutting speeds, and depths for precise material removal, similar to 3D printing but with subtractive rather than additive processes.
  - **Traffic Control**: Managing the flow of vehicles through a network by controlling traffic signals, lane assignments, and speed limits as a sequence of state changes.
  - **Factory Automation**: Defining pick-and-place operations for robotic arms, with states including gripper position, orientation, and open/closed status.
  - **Welding Automation**: Controlling welding paths, speeds, and power settings for automated welding systems, with states including torch position, wire feed rate, and power level.
  - **Laser Processing**: Beyond the included laser cutting examples, controlling laser power, focus, and path for engraving, marking, or material processing.
  - **Bioprinting**: Controlling the deposition of biological materials for tissue engineering, with states including material selection, flow rate, and environmental conditions.

- Creating a custom FullControl implementation for these domains would involve:
  1. Defining domain-specific state objects (e.g., a Drone object instead of a Printer)
  2. Implementing domain-specific output methods (e.g., drone control commands instead of G-code)
  3. Creating domain-specific visualization methods
  4. Developing domain-specific geometry functions for common path patterns

## 2. Directory Structure
```
fullcontrol/
├── __init__.py                 # Main entry point
├── base.py                     # Base classes
├── point.py                    # Point class definition
├── printer.py                  # Printer class definition
├── extrusion_classes.py        # Extrusion-related classes
├── combinations/               # Combined functionality
│   └── gcode_and_visualize/    # Combined G-code and visualization
├── geometry/                   # Geometry functions
│   ├── shapes.py               # Basic shapes
│   ├── waves.py                # Wave functions
│   ├── arcs.py                 # Arc functions
│   └── ...                     # Other geometry functions
├── gcode/                      # G-code generation
│   ├── steps2gcode.py          # Conversion to G-code
│   └── ...                     # Other G-code related modules
└── visualize/                  # Visualization
    ├── steps2visualization.py  # Conversion to visualization
    └── ...                     # Other visualization modules

lab/                            # Experimental features
├── fullcontrol/                # Lab extensions to FullControl
│   ├── fiveaxis.py             # Five-axis printing
│   ├── geometry_model/         # 3D model generation
│   │   ├── steps2geometry.py   # STL output
│   │   └── ...                 # Other geometry model modules
│   └── multiaxis/              # Multi-axis printing
│       └── ...                 # Multi-axis modules

tutorials/                      # Tutorial notebooks
├── overview.ipynb              # Overview of FullControl
└── ...                         # Other tutorials
```

## 3. Core Components

### 3.1 Base Classes and Core Functionality

#### BaseModelPlus (`fullcontrol/base.py`)
- A subclass of Pydantic's BaseModel with additional functionality
- Provides methods for updating attributes from another object
- Includes validators to check if certain attributes are allowed

#### Point (`fullcontrol/point.py` and `fullcontrol/combinations/gcode_and_visualize/classes.py`)
- Represents a 3D point with x, y, z coordinates
- If any coordinate is not defined, the nozzle will not move in that direction
- Optionally includes color for visualization purposes
- Used to define the position of the nozzle

#### Vector (`fullcontrol/vector.py`)
- Represents a 3D vector with x, y, z components
- Used for moving points and defining directions
- Key functions:
  - `move(point, vector)`: Move a point by a vector

#### Extruder (`fullcontrol/combinations/gcode_and_visualize/classes.py`)
- Represents an extruder in a 3D printer
- Key attributes:
  - `on`: Boolean indicating whether the extruder is on or off
  - `units`: Units for E in G-code ('mm' or 'mm3')
  - `dia_feed`: Diameter of the feedstock filament
  - `relative_gcode`: Flag for using relative G-code

#### Fan (`fullcontrol/combinations/gcode_and_visualize/classes.py`)
- Controls the cooling fan of the 3D printer
- Key attributes:
  - `speed_percent`: Fan speed as a percentage (0-100)

#### Hotend (`fullcontrol/combinations/gcode_and_visualize/classes.py`)
- Controls the temperature of the hotend
- Key attributes:
  - `temp`: Temperature in degrees Celsius

#### ExtrusionGeometry (`fullcontrol/combinations/gcode_and_visualize/classes.py`)
- Represents the geometric description of the printed extrudate
- Key attributes:
  - `area_model`: Model for cross-sectional area:
    - 'rectangle': Requires width and height
    - 'stadium': Rectangle with semi-circle at each end, requires width and height
    - 'circle': Requires diameter
    - 'manual': Requires area to be set manually
  - `width`: Width of the printed line (for rectangle or stadium)
  - `height`: Height of the printed line (for rectangle or stadium)
  - `diameter`: Diameter of the printed line (for circle)
  - `area`: Cross-sectional area of the extrudate (automatically calculated unless area_model is 'manual')

#### Printer (`fullcontrol/combinations/gcode_and_visualize/classes.py`)
- Represents a 3D printer
- Key attributes:
  - `print_speed`: Speed at which the printer prints
  - `travel_speed`: Speed at which the printer moves between print locations
  - `new_command`: Dictionary to add new printer commands (e.g., `{'pause': 'M601 ; pause print'}`)

#### Buildplate (`fullcontrol/combinations/gcode_and_visualize/classes.py`)
- Controls the temperature of the build plate
- Key attributes:
  - `temp`: Temperature in degrees Celsius
  - `wait`: Boolean indicating whether to wait for the temperature to be reached before continuing

#### StationaryExtrusion (`fullcontrol/combinations/gcode_and_visualize/classes.py`)
- Extrudes material from the nozzle without moving in XYZ
- Key attributes:
  - `volume`: Volume of material to extrude in mm³
  - `speed`: Speed at which to extrude the material

#### GcodeControls (`fullcontrol/gcode/controls.py`)
- Controls to adjust the style and initialization of the G-code
- Key attributes:
  - `printer_name`: Name of the printer (default: 'generic')
  - `initialization_data`: Values to overwrite default initialization data
  - `save_as`: File name to save the G-code as
  - `include_date`: Whether to include the date in the filename

#### PlotControls (`fullcontrol/visualize/controls.py`)
- Controls to adjust the style of the plot
- Key attributes:
  - `color_type`: Type of color gradient ('manual', 'random_blue', 'z_gradient', 'print_sequence', 'print_sequence_fluctuating')
  - `line_width`: Width of the lines in the plot
  - `style`: Style of the plot ('tube' or 'line')
  - `tube_type`: Type of tube ('flow' or 'cylinders')
  - `hide_travel`: Whether to hide travel lines
  - `hide_annotations`: Whether to hide annotations

### 3.2 Geometry Functions

> **Important Note for LLMs**: All geometry functions return a list of FullControl Point objects (not tuples or other data structures). Any point parameters passed to these functions must also be FullControl Point objects. For complex designs, it may be simpler to work directly with Point objects rather than trying to use the geometry functions with their specific formatting requirements. Geometry functions work best when x, y, and z are all defined for all points.

#### Basic Shapes (`fullcontrol/geometry/shapes.py`)
- `rectangleXY(start_point, x_size, y_size, cw=False)`: Generate a 2D XY rectangle, returns a list of FullControl Point objects
- `circleXY(centre, radius, start_angle, segments=100, cw=False)`: Generate a 2D XY circle, returns a list of FullControl Point objects
- `circleXY_3pt(pt1, pt2, pt3, start_angle=None, start_at_first_point=None, segments=100, cw=False)`: Generate a circle passing through three points, returns a list of FullControl Point objects
- `ellipseXY(centre, a, b, start_angle, segments=100, cw=False)`: Generate a 2D XY ellipse, returns a list of FullControl Point objects
- `polygonXY(centre, enclosing_radius, start_angle, sides, cw=False)`: Generate a 2D XY polygon, returns a list of FullControl Point objects

#### Complex Shapes
- `spiralXY(centre, start_radius, end_radius, start_angle, n_turns, segments, cw=False)`: Generate a 2D XY spiral
- `helixZ(centre, start_radius, end_radius, start_angle, n_turns, pitch_z, segments, cw=False)`: Generate a helix in the Z direction

#### Wave Functions (`fullcontrol/geometry/waves.py`)
- `squarewaveXY(start_point, direction_vector, amplitude, line_spacing, periods, extra_half_period=False, extra_end_line=False)`: Generate a square wave
- `squarewaveXYpolar(start_point, direction_polar, amplitude, line_spacing, periods, extra_half_period=False, extra_end_line=False)`: Generate a square wave using polar coordinates
- `trianglewaveXYpolar(start_point, direction_polar, amplitude, tip_separation, periods, extra_half_period=False)`: Generate a triangle wave
- `sinewaveXYpolar(start_point, direction_polar, amplitude, period_length, periods, segments_per_period=16, extra_half_period=False, phase_shift=0)`: Generate a sine wave
- `segmented_line(start_point, end_point, segments)`: Create a line with multiple segments that can be modified after creation

#### Transformation Functions
- `move(point, vector, copy=False, copy_quantity=1)`: Move a point by a vector, optionally creating copies
- `move_polar(points, centre, radius, angle)`: Move points using polar coordinates
- `travel_to(point)`: Generate a travel move to a point (turns extruder off, moves to the point, then turns extruder back on)

#### Measurement Functions
- `distance(point1, point2)`: Calculate the distance between two points
- `point_to_polar(point, centre)`: Convert a point to polar coordinates relative to a center point
- `angleXY_between_3_points(point1, point2, point3)`: Calculate the angle between three points in the XY plane
- `centreXY_3pt(point1, point2, point3)`: Calculate the center of a circle passing through three points

#### Arc Functions
- `arcXY(centre, radius, start_angle, arc_angle, segments)`: Generate an arc
- `variable_arcXY(centre, start_radius, start_angle, arc_angle, segments, radius_change=0, z_change=0)`: Generate an arc with variable radius and z-height

### 3.3 G-code Generation

#### Steps to G-code Conversion (`fullcontrol/gcode/steps2gcode.py`)
- The `gcode(steps, gcode_controls, show_tips)` function converts a list of steps to G-code
- Process:
  1. Initialize the G-code controls
  2. Create a State object to track the current state
  3. Iterate through each step, calling its `gcode()` method
  4. Append the resulting G-code line to the output
  5. Optionally save the G-code to a file

#### Printer-specific Formatting
- The `printer_name` attribute in GcodeControls determines the printer-specific formatting
- Default is 'generic', but other printers can be specified
- Printer-specific initialization data can be provided

#### State Management
- A `State` object tracks the current state of the printer
- Each step updates the state as needed
- The state includes:
  - Current position
  - Extruder state
  - Printer settings

### 3.4 Visualization

#### Steps to Visualization Conversion (`fullcontrol/visualize/steps2visualization.py`)
- The `visualize(steps, plot_controls, show_tips)` function converts a list of steps to a visualization
- Process:
  1. Initialize the plot controls
  2. Create a State object to track the current state
  3. Create a PlotData object to store the plot data
  4. Iterate through each step, calling its `visualize()` method
  5. Clean up the plot data
  6. Generate the plot using Plotly

#### Plotting and Rendering
- The `plotly.py` module renders the visualization using Plotly
- Two visualization styles are supported:
  - 'line': Simple line representation
  - 'tube': 3D tube representation of the extruded material

#### Visualization Styles and Options
- `color_type`: Controls the coloring of the visualization
- `line_width`: Controls the width of the lines
- `tube_type`: Controls the type of tube ('flow' or 'cylinders')
- `hide_travel`: Controls whether travel moves are shown
- `hide_annotations`: Controls whether annotations are shown

### 3.5 Lab Features

#### Multi-axis Printing
- The lab module includes support for five-axis printing
- Extended Point class with B and C rotational axes
- Inverse kinematics for converting between part coordinates and machine coordinates
- Example: `lab/fullcontrol/fiveaxis.py` and related modules

#### STL Output
- The lab module includes support for generating STL files
- `geometry_model(steps, model_controls)` function in `lab/fullcontrol/geometry_model/steps2geometry.py`
- ModelControls class for controlling STL output options:
  - `stl_filename`: Name of the STL file
  - `tube_shape`: Shape of the tube ('rectangle', 'diamond', 'hexagon', 'octagon')
  - `tube_type`: Type of tube ('flow' or 'cylinders')
  - `stl_type`: Type of STL file ('binary' or 'ascii')

#### Other Experimental Features
- The lab module is for features that aren't suitable for the main package yet
- Features may be more experimental in nature
- Some aspects supplement existing FullControl functionality
- Some aspects overwrite existing functions/classes

### 3.6 Auxiliary Components

#### Annotations
- `PlotAnnotation`: Add annotations to the visualization with a label at specific coordinates
- `GcodeComment`: Add comments to the G-code with options for inline or standalone comments

#### Custom Commands
- `ManualGcode`: Add custom G-code commands by directly specifying the text
- `PrinterCommand`: Execute predefined printer commands by referencing their ID (e.g., 'retract', 'unretract')
  - Each printer has a list of commands that can be called to change state
  - New commands can be added using the `new_command` attribute of a Printer object

## 4. Key Data Flows

### Design to G-code Flow
1. Create a list of steps using geometry functions and state changes
   - **Critical**: Each object in the steps list must be a FullControl object with an implemented `gcode()` method
   - This includes Point, Extruder, ExtrusionGeometry, and other FullControl classes
2. Call `fc.transform(steps, 'gcode', fc.GcodeControls(...))`
3. The transform function calls `gcode()` in `steps2gcode.py`
4. A `State` object tracks the current state
5. Each step calls its `gcode()` method
6. The resulting G-code is returned and optionally saved to a file

### Visualization Flow
1. Create a list of steps using geometry functions and state changes
   - **Critical**: Each object in the steps list must be a FullControl object with an implemented `visualize()` method
   - This includes Point, Extruder, ExtrusionGeometry, and other FullControl classes
2. Call `fc.transform(steps, 'plot', fc.PlotControls(...))`
3. The transform function calls `visualize()` in `steps2visualization.py`
4. A `State` object tracks the current state
5. Each step calls its `visualize()` method
6. The resulting visualization is displayed using Plotly

## 5. Configuration Options

### G-code Generation Options
- `printer_name`: Name of the printer
- `initialization_data`: Custom initialization data
- `save_as`: File name to save the G-code as
- `include_date`: Whether to include the date in the filename

### Visualization Options
- `color_type`: Type of color gradient
- `line_width`: Width of the lines
- `style`: Style of the plot ('tube' or 'line')
- `tube_type`: Type of tube ('flow' or 'cylinders')
- `hide_travel`: Whether to hide travel lines
- `hide_annotations`: Whether to hide annotations

### Printer Settings
- `print_speed`: Speed at which the printer prints
- `travel_speed`: Speed at which the printer moves between print locations

### STL Output Options
- `stl_filename`: Name of the STL file
- `tube_shape`: Shape of the tube
- `tube_type`: Type of tube
- `stl_type`: Type of STL file

## 6. Usage Patterns

> **Note for LLMs**: When working with FullControl, remember that:
> 1. All objects in the steps list must be FullControl objects with `gcode()` and `visualize()` methods
> 2. Geometry functions return lists of FullControl Point objects that can be extended with other FullControl objects
> 3. The `gcode()` and `visualize()` methods are inherited or supplemented to a parent class, allowing for extensibility
> 4. For complex designs, it may be simpler to work directly with Point objects rather than using geometry functions

### Basic Usage Example
```python
import fullcontrol as fc

# Define design parameters
layer_height = 0.2

# Create a list of steps
steps = []
steps.append(fc.Point(x=0, y=0, z=0))
steps.append(fc.Point(x=10, y=0, z=0))
steps.append(fc.Point(x=10, y=10, z=0))
steps.append(fc.Point(x=0, y=10, z=0))
steps.append(fc.Point(x=0, y=0, z=layer_height))

# For visualization
fc.transform(steps, 'plot', fc.PlotControls(style='line'))

# For G-code
gcode = fc.transform(steps, 'gcode', fc.GcodeControls(
    printer_name='prusa_i3',
    save_as='my_design',
    initialization_data={
        'print_speed': 1000,
        'nozzle_temp': 210,
        'bed_temp': 60
    }
))
```

### Common Design Patterns
- Using loops to create repetitive patterns
- Using mathematical functions to create complex geometries
- Using state changes to control printer behavior (extruder on/off, fan speed, temperature, etc.)
- Using annotations to add information to the visualization and G-code
- Using travel_to() for non-printing moves between printing operations

### Advanced Usage Examples
- Multi-axis printing using the lab module
- Generating STL files using the lab module
- Creating custom printer definitions
- Using complex geometry functions to create intricate designs

## 7. Key Algorithms

### Path Generation
- Basic shapes: rectangles, circles, polygons
- Complex shapes: spirals, helices, arcs
- Wave functions: square waves, triangle waves, sine waves
- Transformation functions: move, move_polar, travel_to

### Extrusion Calculation
- Based on the cross-sectional area of the extrudate
- Different area models: rectangle, stadium, circle, manual
- Calculation of E values for G-code

### Inverse Kinematics
- For multi-axis printing
- Converting between part coordinates and machine coordinates

## 8. Module Dependencies

- `fullcontrol/combinations/gcode_and_visualize/common.py` imports from:
  - `.classes`
  - `fullcontrol.common`
  - `fullcontrol.geometry`
  - `fullcontrol.visualize.bounding_box`

- `fullcontrol/combinations/gcode_and_visualize/classes.py` imports from:
  - `fullcontrol.gcode`
  - `fullcontrol.visualize`
  - `fullcontrol.base`

- `fullcontrol/geometry/__init__.py` imports from:
  - `fullcontrol.combinations.gcode_and_visualize.classes`
  - Various geometry modules

- `fullcontrol/gcode/steps2gcode.py` imports from:
  - `fullcontrol.gcode.point`
  - `fullcontrol.gcode.printer`
  - `fullcontrol.gcode.extrusion_classes`
  - `fullcontrol.gcode.state`
  - `fullcontrol.gcode.controls`

- `fullcontrol/visualize/steps2visualization.py` imports from:
  - `fullcontrol.visualize.state`
  - `fullcontrol.visualize.plot_data`
  - `fullcontrol.visualize.controls`
  - `fullcontrol.visualize.tips`

## 9. Common Modification Patterns

### Adding New Printers
- Create a new printer definition in the appropriate module
- Define printer-specific G-code formatting
- Define printer-specific initialization data

### Creating Custom Geometry Functions
- Create a new function that returns a list of Points
- Use existing geometry functions as building blocks
- Follow the pattern of existing geometry functions

### Adding New State Objects
- Create a new class that inherits from BaseModelPlus
- Implement the `gcode()` and `visualize()` methods
- Follow the pattern of existing state objects
- This extensibility is a core design principle of FullControl, allowing for future methods beyond G-code and visualization

## 10. Performance Considerations

### Factors Affecting Performance
- Number of steps in the design
- Complexity of the geometry
- Number of segments in curved shapes
- Visualization style ('tube' is more resource-intensive than 'line')

### Optimization Tips
- Use an appropriate number of segments for curved shapes
- Use the 'line' visualization style for large designs
- Use the 'cylinders' tube type for more accurate but less smooth STL output
- Use the 'flow' tube type for smoother but less accurate STL output

## 11. Class Responsibility Map

This section maps which classes are responsible for generating different aspects of the G-code and visualization output. Understanding these responsibilities helps in identifying which classes to modify for specific customizations.

### G-code Generation Responsibilities

Class | Primary Responsibility | File Location |
|-------|------------------------|---------------|
`Point` | Generates movement commands (position changes) | `fullcontrol/gcode/point.py` |
`Extruder` | Controls extrusion parameters and formatting | `fullcontrol/gcode/extrusion_classes.py` |
`ExtrusionGeometry` | Defines cross-sectional geometry for extrusion calculations | `fullcontrol/gcode/extrusion_classes.py` |
`Printer` | Manages printer settings and speed parameters | `fullcontrol/gcode/printer.py` |
`Fan` | Controls cooling fan settings | `fullcontrol/gcode/auxilliary_components.py` |
`Hotend` | Controls hotend temperature settings | `fullcontrol/gcode/auxilliary_components.py` |
`Buildplate` | Controls build plate temperature settings | `fullcontrol/gcode/auxilliary_components.py` |
`StationaryExtrusion` | Manages extrusion without XYZ movement | `fullcontrol/gcode/extrusion_classes.py` |
`GcodeComment` | Adds comments to G-code output | `fullcontrol/gcode/annotations.py` |
`ManualGcode` | Inserts custom G-code commands | `fullcontrol/gcode/auxilliary_components.py` |
`PrinterCommand` | Executes predefined printer commands | `fullcontrol/gcode/commands.py` |

### Visualization Responsibilities

Class | Primary Responsibility | File Location |
|-------|------------------------|---------------|
`Point` | Defines positions for visualization | `fullcontrol/visualize/point.py` |
`Extruder` | Controls whether lines are drawn as extrusion or travel | `fullcontrol/visualize/extrusion_classes.py` |
`ExtrusionGeometry` | Defines geometry for visualization | `fullcontrol/visualize/extrusion_classes.py` |
`PlotAnnotation` | Adds annotations to visualization | `fullcontrol/visualize/annotations.py` |

## 12. Parameter-to-Effect Tables

These tables map specific parameters to their effects on G-code output and visualization. This helps in identifying which parameters to modify for specific customizations.

### Extruder Parameters

Parameter | Effect on Output | Default |
|-----------|------------------|---------|
`on` | Controls whether extrusion occurs (True) or not (False) | None |
`units` | Sets units for E in G-code ('mm' or 'mm3') | None |
`dia_feed` | Sets diameter of feedstock filament for extrusion calculations | None |
`relative_gcode` | Controls whether extrusion is relative (True) or absolute (False) | None |
`travel_format` | Controls formatting of travel moves (e.g., 'G1_E0' uses G1 with E0 instead of G0) | None |
`volume_to_e` | Factor to convert volume to E value (calculated automatically) | None |
`total_volume` | Tracks current extrusion volume (calculated automatically) | None |
`total_volume_ref` | Reference point for relative extrusion (calculated automatically) | None |

### Printer Parameters

Parameter | Effect on Output | Default |
|-----------|------------------|---------|
`print_speed` | Sets speed for printing moves | None |
`travel_speed` | Sets speed for non-printing moves | None |
`new_command` | Dictionary to add custom printer commands | None |

### ExtrusionGeometry Parameters

Parameter | Effect on Output | Default |
|-----------|------------------|---------|
`area_model` | Sets model for cross-sectional area calculation | None |
`width` | Sets width of printed line (for rectangle or stadium models) | None |
`height` | Sets height of printed line (for rectangle or stadium models) | None |
`diameter` | Sets diameter of printed line (for circle model) | None |
`area` | Sets cross-sectional area directly (for manual model) | None |

### GcodeControls Parameters

Parameter | Effect on Output | Default |
|-----------|------------------|---------|
`printer_name` | Sets printer-specific formatting | 'generic' |
`initialization_data` | Overrides default initialization data | {} |
`save_as` | Sets filename for saving G-code | None |
`include_date` | Controls whether date is included in filename | True |

## 13. Code Flow and Interaction Patterns

This section describes how objects interact during G-code generation and visualization, helping to understand the flow of data and control.

### G-code Generation Flow

1. User creates a list of steps (FullControl objects)
2. User calls `fc.transform(steps, 'gcode', controls)`
3. The transform function calls `gcode()` in `steps2gcode.py`
4. A `State` object is created to track the current state
5. For each step in the list:
   - The step's `gcode()` method is called with the current state
   - The state is updated based on the step
   - The resulting G-code line is appended to the output
6. The complete G-code is returned and optionally saved to a file

### Key Interaction Patterns

- **State Updates**: Each object's `gcode()` method updates the state object, which affects how subsequent objects generate G-code
- **Inheritance Chain**: The `gcode()` method may be inherited from a parent class or implemented directly
- **Parameter Propagation**: Parameters set on one object (e.g., Extruder) affect how other objects (e.g., Point) generate G-code
- **Conditional Logic**: Objects may generate different G-code based on the current state (e.g., Point generates G0 or G1 based on Extruder state)

### Example: Point and Extruder Interaction

When a Point object's `gcode()` method is called:
1. It checks if movement occurs by comparing its coordinates to the current position
2. It determines whether to use G0 or G1 based on the Extruder's `on` state and `travel_format` property
3. It gets the F value (speed) from the Printer object in the state
4. It gets the E value (extrusion amount) from the Extruder object in the state
5. It combines these values into a G-code line
6. It updates the current position in the state

## 14. Inheritance and Composition Relationships

Understanding the inheritance and composition relationships between classes helps in identifying which classes to modify for specific customizations.

### Inheritance Hierarchy

- **BaseModelPlus** (base.py): The root class for all FullControl objects
  - **Point** (point.py → gcode/point.py + visualize/point.py → combinations/gcode_and_visualize/classes.py)
  - **Extruder** (common.py → gcode/extrusion_classes.py + visualize/extrusion_classes.py → combinations/gcode_and_visualize/classes.py)
  - **ExtrusionGeometry** (common.py → gcode/extrusion_classes.py + visualize/extrusion_classes.py → combinations/gcode_and_visualize/classes.py)
  - **Printer** (printer.py → gcode/printer.py → combinations/gcode_and_visualize/classes.py)
  - **Fan**, **Hotend**, **Buildplate** (similar pattern to above)
  - **GcodeControls**, **PlotControls** (controls.py in respective directories)

### Composition Relationships

- **State** contains:
  - Point (current position)
  - Extruder (current extruder state)
  - ExtrusionGeometry (current extrusion geometry)
  - Printer (current printer settings)
  - Other state objects (Fan, Hotend, Buildplate, etc.)

- **GcodeControls** contains:
  - printer_name
  - initialization_data
  - save_as
  - include_date

## 15. Common Modification Patterns with Examples

This section provides more detailed examples of common modifications to help identify patterns for specific customizations.

### Modifying G-code Output Format

To change how G-code is formatted, you typically need to:
1. Identify which class generates the relevant G-code (see Class Responsibility Map)
2. Determine which parameter controls the formatting (see Parameter-to-Effect Tables)
3. Set that parameter in your script

Example: Changing travel move format
```python
import fullcontrol as fc

# Create extruder with custom travel_format
extruder = fc.Extruder(
    on=True,
    travel_format="G1_E0"  # Use G1 with E0 instead of G0 for travel moves
)

# Add to steps list
steps = [extruder, ...]
```

### Adding Custom Printer Commands

To add custom printer commands:
1. Create a Printer object with custom commands
2. Add the Printer object to your steps list

Example: Adding a custom pause command
```python
import fullcontrol as fc

# Create printer with custom command
printer = fc.Printer(
    print_speed=1000,
    travel_speed=3000,
    new_command={'pause': 'M601 ; pause print'}
)

# Add to steps list
steps = [printer, ...]

# Use the custom command later
steps.append(fc.PrinterCommand(id='pause'))
```

### Customizing Extrusion Calculation

To customize how extrusion is calculated:
1. Create an ExtrusionGeometry object with your desired parameters
2. Add it to your steps list

Example: Setting custom extrusion width and height
```python
import fullcontrol as fc

# Create extrusion geometry
extrusion_geometry = fc.ExtrusionGeometry(
    area_model='rectangle',
    width=0.4,
    height=0.2
)

# Add to steps list
steps = [extrusion_geometry, ...]
```

## 16. Anti-patterns and Common Pitfalls

This section describes approaches to avoid and common mistakes when working with FullControl.

### Anti-patterns

1. **Using ManualGcode for Systematic Changes**:
   - **Problem**: ManualGcode bypasses FullControl's state tracking system and inserts raw G-code directly.
   - **Why it's bad**: This breaks the connection between the design (steps list) and the G-code output, making it impossible for FullControl to maintain consistent state.
   - **Example**: Using ManualGcode to change all G1 commands to G01 will result in inconsistent G-code because subsequent Point objects will still generate G1 commands.
   - **Better approach**: Modify the appropriate class's `gcode()` method or use proper configuration parameters.

2. **Using Printer.new_command to Override Core Movement Commands**:
   - **Problem**: Attempting to override basic movement commands (like G0/G1) using Printer.new_command.
   - **Why it's bad**: The Point class directly generates movement commands without using these custom commands, so they won't be used for normal movements.
   - **Better approach**: For formatting changes to core G-code commands, either:
     - Create a proper printer definition in the appropriate module
     - Post-process the complete G-code after generation (outside of FullControl)
     - Extend the Point class with a custom implementation

3. **Modifying Printer Definitions for One-off Changes**:
   - **Problem**: Creating a custom printer definition just to change a few settings.
   - **Why it's bad**: Unnecessarily complex and can lead to maintenance issues.
   - **Better approach**: Use the initialization_data parameter of GcodeControls.

4. **Direct Manipulation of G-code During Generation**:
   - **Problem**: Trying to manipulate G-code during the generation process.
   - **Why it's bad**: Disrupts FullControl's state tracking and can lead to inconsistent output.
   - **Better approach**: Customize the generation process by setting appropriate parameters on FullControl objects.

5. **Ignoring State Management**:
   - **Problem**: Not considering how objects update the state and affect subsequent objects.
   - **Why it's bad**: Can lead to unexpected results and inconsistent G-code.
   - **Better approach**: Understand the state flow and how each object's `gcode()` method affects the state.

### Common Pitfalls

1. **Incomplete Steps List**: Missing essential objects in the steps list (e.g., Extruder, ExtrusionGeometry) can lead to incomplete or incorrect G-code.

2. **Incorrect Parameter Types**: Setting parameters with incorrect types can cause errors or unexpected behavior.

3. **Inconsistent State**: Setting conflicting parameters on different objects can lead to inconsistent state and unexpected G-code.

4. **Ignoring Return Values**: Some methods return new objects or lists that need to be incorporated into the steps list.

## 17. Decision Tree for Customizations

This decision tree helps identify which class and parameter to modify for specific customizations.

### G-code Output Customization

1. **Want to change how movement is formatted?**
   - Modify Point.gcode() or set Extruder.travel_format

2. **Want to change how extrusion is calculated?**
   - Modify ExtrusionGeometry parameters (area_model, width, height, diameter, area)
   - Or modify Extruder parameters (units, dia_feed, relative_gcode)

3. **Want to change printer speeds?**
   - Modify Printer parameters (print_speed, travel_speed)

4. **Want to add custom G-code commands?**
   - Use ManualGcode for one-off commands
   - Use Printer.new_command and PrinterCommand for reusable commands

5. **Want to change printer-specific initialization?**
   - Modify GcodeControls.initialization_data

### Visualization Customization

1. **Want to change how the visualization looks?**
   - Modify PlotControls parameters (color_type, line_width, style, tube_type, etc.)

2. **Want to add annotations to the visualization?**
   - Use PlotAnnotation

3. **Want to change how extrusion is visualized?**
   - Modify ExtrusionGeometry parameters (width, height, diameter, area_model)

## 18. Complete Property Listings

This section provides complete listings of all properties for key classes, including those that might not be documented elsewhere.

### Point Properties

- `x`: X-coordinate (float or None)
- `y`: Y-coordinate (float or None)
- `z`: Z-coordinate (float or None)
- `color`: Color for visualization [r, g, b] (list or None)

### Extruder Properties

- `on`: Whether extrusion is on (bool or None)
- `units`: Units for E in G-code ('mm' or 'mm3' or None)
- `dia_feed`: Diameter of feedstock filament (float or None)
- `relative_gcode`: Whether to use relative G-code (bool or None)
- `volume_to_e`: Factor to convert volume to E value (float or None, calculated)
- `total_volume`: Current extrusion volume (float or None, calculated)
- `total_volume_ref`: Reference for relative extrusion (float or None, calculated)
- `travel_format`: Format for travel moves (str or None)

### ExtrusionGeometry Properties

- `area_model`: Model for cross-sectional area ('rectangle', 'stadium', 'circle', 'manual', or None)
- `width`: Width of printed line (float or None)
- `height`: Height of printed line (float or None)
- `diameter`: Diameter of printed line (float or None)
- `area`: Cross-sectional area (float or None, calculated unless area_model is 'manual')

### Printer Properties

- `print_speed`: Speed for printing moves (float or None)
- `travel_speed`: Speed for non-printing moves (float or None)
- `new_command`: Dictionary of custom commands (dict or None)
- `speed_changed`: Whether speed has changed (bool, internal use)

### GcodeControls Properties

- `printer_name`: Name of printer (str, default: 'generic')
- `initialization_data`: Custom initialization data (dict, default: {})
- `save_as`: Filename for saving G-code (str or None, default: None)
- `include_date`: Whether to include date in filename (bool, default: True)

## 19. Cross-Reference Index

This index helps quickly find which class and method control specific aspects of G-code generation and visualization.

### G-code Features

- **Movement Commands (G0/G1)**: Point.gcode(), Extruder.travel_format
- **Extrusion Amount (E)**: Extruder.e_gcode(), ExtrusionGeometry.area
- **Speed (F)**: Printer.f_gcode(), Printer.print_speed, Printer.travel_speed
- **Temperature**: Hotend.gcode(), Buildplate.gcode()
- **Fan Control**: Fan.gcode()
- **Comments**: GcodeComment.gcode()
- **Custom Commands**: ManualGcode.gcode(), PrinterCommand.gcode()
- **Relative/Absolute Extrusion**: Extruder.relative_gcode

### Visualization Features

- **Line Color**: Point.color, PlotControls.color_type
- **Line Width**: PlotControls.line_width
- **Tube Style**: PlotControls.style, PlotControls.tube_type
- **Annotations**: PlotAnnotation.visualize()
- **Travel Lines**: PlotControls.hide_travel
- **Axes**: PlotControls.hide_axes

## 20. G-code Formatting Modifications

This section provides guidance on how to properly modify G-code formatting in FullControl, addressing common formatting requirements.

### Understanding G-code Generation in FullControl

In FullControl, G-code is generated by the `gcode()` method of each object in the steps list. The most important classes for G-code formatting are:

1. **Point**: Generates movement commands (G0/G1)
2. **Extruder**: Controls extrusion parameters and adds E values
3. **Printer**: Provides speed values (F)

Each of these classes has a specific role in generating G-code, and they work together through the shared State object.

### Approaches to Modifying G-code Format

#### 1. For Standard Formatting Changes

If you need to change standard aspects of G-code formatting (like using G1 instead of G0 for travel moves), use the built-in parameters:

```python
# Example: Using G1 E0 instead of G0 for travel moves
extruder = fc.Extruder(
    on=True,
    travel_format="G1_E0"
)
```

#### 2. For Custom Printer-Specific Formatting

If you need printer-specific formatting, use the appropriate printer definition:

```python
# Example: Using a specific printer definition
gcode = fc.transform(steps, 'gcode', fc.GcodeControls(
    printer_name='prusa_i3'
))
```

#### 3. For Advanced Formatting Changes (Zero-padding, etc.)

For advanced formatting changes that aren't supported by built-in parameters (like changing G1 to G01):

**Option A: Post-processing** (Recommended for simple formatting changes)
```python
# Generate G-code normally
gcode = fc.transform(steps, 'gcode', controls)

# Post-process to add zero-padding to G-codes
gcode = gcode.replace("G0 ", "G00 ").replace("G1 ", "G01 ")

# Save the modified G-code
with open("modified_gcode.gcode", "w") as f:
    f.write(gcode)
```

**Option B: Custom Point Class** (For more complex changes)
```python
# Create a custom Point class that overrides the gcode method
class CustomPoint(fc.Point):
    def gcode(self, state):
        # Get the original G-code from the parent class
        original_gcode = super().gcode(state)
        
        # Replace G1 with G01 and G0 with G00
        if original_gcode:
            original_gcode = original_gcode.replace("G0 ", "G00 ").replace("G1 ", "G01 ")
        
        return original_gcode

# Use the custom Point class in your design
steps = []
steps.append(CustomPoint(x=0, y=0, z=0))
# ...
```

### What NOT to Do

1. **Don't use ManualGcode for systematic formatting changes**:
   ```python
   # DON'T DO THIS - it will break state tracking
   steps.append(fc.ManualGcode("G01 X10 Y10 Z0"))
   ```

2. **Don't override core movement commands with Printer.new_command**:
   ```python
   # DON'T DO THIS - it won't affect Point-generated commands
   printer = fc.Printer(
       new_command={
           'print_move': 'G01 X{x} Y{y} Z{z} F{f} E{e}'
       }
   )
   ```

3. **Don't mix manual and automatic G-code generation**:
   ```python
   # DON'T DO THIS - inconsistent formatting
   steps.append(fc.ManualGcode("G01 X0 Y0 Z0"))
   steps.append(fc.Point(x=10, y=10, z=0))  # Will generate G1, not G01
   ```