import asyncio
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from pythonosc import dispatcher, osc_server

from logger import setup_logger

logging = setup_logger("Visualizer")


class Visualize:
    def __init__(self, data, app, socketio):
        self.data = data
        self.app = app
        self.socketio = socketio
        self.cursor = np.mean(self.data, axis=0)
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/cursor", self.update_cursor)

    def update_cursor(self, _, x, y, z):
        logging.info(f"Received cursor data: {x}, {y}, {z}")
        self.cursor[0] = x
        self.cursor[1] = y
        self.cursor[2] = z
        self.socketio.emit("update_cursor", {"x": x, "y": y, "z": z})
        self.interpolator.send_data(self.osc_client, self.get_cursor_position())

    def get_cursor_position(self):
        return np.array(self.cursor[:])

    def get_data_min_max(self):
        min_xyz = np.min(self.data, axis=0).tolist()
        max_xyz = np.max(self.data, axis=0).tolist()
        return min_xyz + max_xyz

    def start_osc_server(self, ip, port):
        try:
            server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)
            logging.info(f"Serving on {server.server_address}")
            server.serve_forever()
        except Exception as e:
            logging.error(f"Error starting OSC server: {e}")

    def show(self):
        self.socketio.run(self.app, debug=False)

    async def run(self, ip, port, interpolator, osc_client):
        self.interpolator = interpolator
        self.osc_client = osc_client
        loop = asyncio.get_event_loop()

        # self.osc_client.send_message("/min_max", self.get_data_min_max())

        with ThreadPoolExecutor() as executor:
            loop.run_in_executor(executor, self.start_osc_server, ip, port)
            loop.run_in_executor(executor, self.show)
