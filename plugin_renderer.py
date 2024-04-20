import argparse
import reapy
import time

from reapy import reascript_api as RPR


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--mode',
                      dest='value_generation_mode',
                      type=str,
                      default='preset')
    
    return parser.parse_args()


# Link and get current project
reapy.connect()
project = reapy.Project()

# Get track and plugin
track = project.tracks[0]
plugin = track.fxs[0]

# Get preset no. 
num_presets = plugin.n_presets
for i in range(num_presets):

    name = plugin.preset
    print(f'Name {name}')
    plugin.preset = i
    # Get and print all parameter values for the current preset
    for j in range(plugin.n_params):
        param = plugin.params[j]
        param_value = RPR.TrackFX_GetParam(track.id, plugin.index, j, 0.0, 1.0)
        print(f'Parameter {j}: {param.name}, Value: {param_value[0]}') # get only current value

    project.cursor_position = 0
    RPR.CSurf_OnPlay()

    time.sleep(2)

    RPR.CSurf_OnStop()
