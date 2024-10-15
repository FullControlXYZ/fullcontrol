from fullcontrol.visualize.controls import PlotControls

def tips(controls: PlotControls):
    tip_str = ''
    if controls.style == 'tube' and controls.raw_data == False:
            if 'extrusion_width' not in controls.initialization_data.keys() or 'extrusion_height' not in controls.initialization_data.keys():
                tip_str += "\ntip: set initial `extrusion_width` and `extrusion_height` in the initialization_data to ensure the preview is correct:\n   - `fc.transform(..., controls=fc.PlotControls(initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))`"
    if tip_str != '':
        print('fc.transform guidance tips are being written to screen if any potential issues are found - hide tips with fc.transform(..., show_tips=False)' + tip_str + '\n')
