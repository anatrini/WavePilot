import argparse
import numpy as np
import sounddevice as sd
import threading

from pythonosc import dispatcher, osc_server
from scipy.io.wavfile import write



def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--device_id',
                      dest='device_id',
                      type=int,
                      default=0)
    
    parser.add_argument('-f', '--fs',
                      dest='fs',
                      type=int,
                      default=44100)
    
    parser.add_argument('-b', '--blocksize',
                      dest='blocksize',
                      type=int,
                      default=2048)
    
    parser.add_argument('-s', '--silence_thresh',
                      dest='silence_thresh',
                      type=float,
                      default=1e-6)
    
    parser.add_argument('-t', '--timeout',
                      dest='timeout',
                      type=int,
                      default=30)
    
    return parser.parse_args()



class Recorder:
    def __init__(self, device_id, fs, blocksize, silence_thresh, timeout):
        self.device_id = device_id
        self.fs = fs
        self.blocksize = blocksize
        self.silence_thresh = silence_thresh
        self.timeout = timeout

        self.stream = None
        self.recording = np.array([])
        self.filepath = None
        self.timer = None

    def handle_timeout(self, signum, frame):
        print('Timeout, exiting...')
        exit(0)

    def reset_timer(self):
        if self.timer is not None:
            self.timer.cancel()
        self.timer = threading.Timer(self.timeout, self.handle_timeout)
        self.timer.start()

    def callback(self, indata, frames, time, status):
        self.recording = np.append(self.recording, indata)

    def start_recording(self, unused_addr):
        self.reset_timer()
        print('Record starts...')
        self.stream = sd.InputStream(callback=self.callback, 
                                      channels=1, 
                                      samplerate=self.fs, 
                                      device=self.device_id,
                                      blocksize=self.blocksize)
        self.stream.start()

    def stop_recording(self, unused_addr):
        self.reset_timer()
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None

            energy = np.sum(self.recording**2)
            if energy > self.silence_thresh:
                print(f'Writing audio at {self.filepath}')
                write(self.filepath, self.fs, self.recording)
            else:
                print(f'No incoming audio!')
            self.recording = np.array([])
        else:
            print("No active stream to stop.")

        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def set_filepath(self, unused_addr, path):
        self.reset_timer()
        self.filepath = path
        print(f'Set filepath to {self.filepath}')


def main():

    IP_ADDRESS = '127.0.0.1'
    PORT = 5005

    args = get_arguments()

    device_id = args.device_id
    fs = args.fs
    blocksize = args.blocksize
    silence_thresh = args.silence_thresh
    timeout = args.timeout

    # devices = sd.query_devices()
    # device_id = None
    # for i, device in enumerate(devices):
    #     print(f"Device {i}: {device['name']}")
    #     if device['name'] == 'Blackhole':
    #         device_id = i

    # if device_id is None:
    #     raise Exception('No Blackhole device available')

    recorder = Recorder(device_id=device_id, fs=fs, blocksize=blocksize, silence_thresh=silence_thresh, timeout=timeout)

    dispatcher_ = dispatcher.Dispatcher()
    dispatcher_.map('/filepath', recorder.set_filepath)
    dispatcher_.map('/start', recorder.start_recording)
    dispatcher_.map('/stop', recorder.stop_recording)

    server = osc_server.ThreadingOSCUDPServer((IP_ADDRESS, PORT), dispatcher_)
    print(f'Serving on {server.server_address}')
    server.serve_forever()



if __name__ == '__main__':
    main()