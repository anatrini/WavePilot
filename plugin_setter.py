import reapy
import numpy as np
import queue
import threading

from logger import setup_logger
from pythonosc import dispatcher, osc_server
from reapy import reascript_api as RPR


logging = setup_logger('Plugin setter')

# Create a queue for incoming data packages
data_queue = queue.Queue()


def process_data():
    while True:
        # Take one data package from the queue and process it
        params = data_queue.get()
        print(params)
        with reapy.inside_reaper():
            # Link and get current project
            reapy.connect()
            project = reapy.Project()

            # Get track and plugin
            track = project.tracks[0]
            plugin = track.fxs[0]

            for i, value in enumerate(params):
                RPR.TrackFX_SetParam(track.id, plugin.index, i, value)

        # Confirm data package has been processed
        data_queue.task_done()



def set_plugin_params(unused_addr, *args):
    # Convert args to numpy array
    params = np.array(args)
    data_queue.put(params)


# Set up OSC dispatcher and server
dispatcher = dispatcher.Dispatcher()
dispatcher.map('/interpolated_data', set_plugin_params)

server = osc_server.ThreadingOSCUDPServer(('localhost', 5106), dispatcher)
logging.info(f'Serving on: {server.server_address}')

data_thread = threading.Thread(target=process_data)
data_thread.start()

server.serve_forever()
