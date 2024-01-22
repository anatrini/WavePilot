import numpy as np

from logger import setup_logger
from scipy.interpolate import RBFInterpolator

logging = setup_logger('Radial Basis Function Interpolator')


class RBFInterpolation:
    def __init__(self, reduced_data, original_data, smoothing, kernel, epsilon):
        self.reduced_data = reduced_data
        self.original_data = original_data
        self.smoothing = smoothing
        self.kernel = kernel
        self.epsilon = epsilon
        self.interpolator = RBFInterpolator(self.reduced_data, self.original_data, smoothing=self.smoothing, kernel=self.kernel, epsilon=self.epsilon)
        
        self.minX = np.min(reduced_data[:, 0])
        self.maxX = np.max(reduced_data[:, 0])
        self.minY = np.min(reduced_data[:, 1])
        self.maxY = np.max(reduced_data[:, 1])
        self.minZ = np.min(reduced_data[:, 2])
        self.maxZ = np.max(reduced_data[:, 2])

    # Denormalize cursor position so cursor position will correspond when moved in the 3D graph
    # While at the same time, once denormalized, can be properly used for the interpolation
    def denormalize(self, cursor_position):
        denormalized_position = [0, 0, 0]
        denormalized_position[0] = (cursor_position[0] + 1) / 2 * (self.maxX - self.minX) + self.minX
        denormalized_position[1] = (cursor_position[1] + 1) / 2 * (self.maxY - self.minY) + self.minY
        denormalized_position[2] = (cursor_position[2] + 1) / 2 * (self.maxZ - self.minZ) + self.minZ
        return denormalized_position

    def interpolate(self, cursor_position):
        # Get cursor's position from visualizer
        cursor_position = self.denormalize(cursor_position)
        cursor_position = np.array(cursor_position).reshape(1, -1)
        interpolated_data = self.interpolator(cursor_position)
        interpolated_data = np.clip(interpolated_data, 0, 1)
        return interpolated_data
    
    def send_data(self, osc_client, cursor_position):
        interpolated_data = self.interpolate(cursor_position)
        logging.info(f'Interpolated Data: {interpolated_data}')
        osc_client.send_message("/interpolated_data", interpolated_data.flatten().tolist())