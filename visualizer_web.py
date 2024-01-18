import asyncio
import numpy as np

from concurrent.futures import ThreadPoolExecutor
from pythonosc import dispatcher, osc_server

class Visualizer():
    def __init__(self, data, app, socketio):
        self.data = data
        self.app = app
        self.socketio = socketio
        self.cursor = np.mean(self.data, axis=0)
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map('/cursor', self.update_cursor)

    def update_cursor(self, _, x, y, z):
        print(f"Received cursor data: {x}, {y}, {z}")
        self.cursor[0] = x
        self.cursor[1] = y
        self.cursor[2] = z
        self.socketio.emit('update_cursor', {'x': x, 'y': y, 'z': z})

    def get_cursor_position(self):
        return np.array(self.cursor[:])
    
    def start_osc_server(self, ip, port):
        try:
            server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)
            print(f'Serving on {server.server_address}')
            server.serve_forever()
        except Exception as e:
            print(f"Error starting OSC server: {e}")

    def show(self):
        self.socketio.run(self.app, debug=False)

    async def run(self, ip, port):
        loop = asyncio.get_event_loop()

        with ThreadPoolExecutor() as executor:
            await asyncio.gather(
                loop.run_in_executor(executor, self.start_osc_server, ip, port),
                loop.run_in_executor(executor, self.show)
            )