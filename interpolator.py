import numpy as np

from logger import setup_logger
from scipy.interpolate import RBFInterpolator

logging = setup_logger('Radial Basis Function Interpolator')


class RBFInterpolation:
    def __init__(self, reduced_data, original_data, kernel, epsilon):
        self.reduced_data = reduced_data
        self.original_data = original_data
        self.kernel = kernel
        self.epsilon = epsilon
        self.interpolator = RBFInterpolator(self.reduced_data, self.original_data, kernel=self.kernel, epsilon=self.epsilon)

    def interpolate(self, cursor_position):
        # Get cursor's position from visualizer
        cursor_position = np.array(cursor_position).reshape(1, -1)
        return self.interpolator(cursor_position)
    
    def send_data(self, osc_client, cursor_position):
        interpolated_data = self.interpolate(cursor_position)
        logging.info(f'Interpolated Data: {interpolated_data}')
        osc_client.send_message("/interpolated_data", interpolated_data.flatten().tolist())