import asyncio
import logging
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go

from concurrent.futures import ThreadPoolExecutor
from pythonosc import dispatcher, osc_server

UPDATE_INT = 500


class Visualizer():
    def __init__(self, data):
        self.data = data
        self.cursor = np.mean(self.data, axis=0)
        self.app = dash.Dash(__name__)
        self.app.layout = html.Div([
            dcc.Graph(id='presets-graph', animate=True),
            dcc.Interval(
                id='graph-update',
                interval=UPDATE_INT
            ),
        ])
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map('/cursor', self.update_cursor)

        @self.app.callback(Output('presets-graph', 'figure'),
                           [Input('graph-update', 'n_intervals')])
        def update_graph_scatter(n):
            # Normalize data for color coding
            normalized_data = (self.data - np.min(self.data, axis=0)) / (np.max(self.data, axis=0) - np.min(self.data, axis=0))
            colors = np.array(normalized_data * 255, dtype=np.uint8)
            cursor_position = self.get_cursor_position()
            trace = go.Scatter3d(
                x=self.data[:, 0],
                y=self.data[:, 1],
                z=self.data[:, 2],
                mode='markers',
                marker=dict(
                    size=8,
                    color=[f'rgb({r},{g},{b})' for r, g, b in colors],
                    opacity=0.8
                )
            )
            cursor_pos = cursor_position.tolist()
            cursor = go.Scatter3d(
                x=[cursor_pos[0]],
                y=[cursor_pos[1]],
                z=[cursor_pos[2]],
                mode='markers',
                marker=dict(
                    color='rgb(255, 0, 0)',
                    size=12,
                    symbol='circle',
                    line=dict(
                        color='rgb(204, 204, 204)',
                        width=1
                    ),
                    opacity=0.9
                )
            )
            layout = go.Layout(
                margin=dict(
                    l=0,
                    r=0,
                    b=0,
                    t=0
                )
            )
            return {'data': [trace, cursor], 'layout': layout}
        
    def update_cursor(self, _, x, y, z):
        print(f"Received cursor data: {x}, {y}, {z}")
        global cursor
        self.cursor[0] = x
        self.cursor[1] = y
        self.cursor[2] = z

    def get_cursor_position(self):
        return np.array(self.cursor[:])
    
    def start_osc_server(self, ip, port):
        server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)
        print(f'Serving on {server.server_address}')
        server.serve_forever()

    def show(self):
        log = logging.getLogger('werkzeug')
        log.disabled = True
        self.app.run_server(debug=False)

    async def run(self, ip, port):
        loop = asyncio.get_event_loop()

        with ThreadPoolExecutor() as executor:
            await asyncio.gather(
                loop.run_in_executor(executor, self.start_osc_server, ip, port),
                loop.run_in_executor(executor, self.show)
            )