import argparse
import datetime
import os
import random
import signal
import time

import numpy as np
import pandas as pd
import reapy
import sounddevice as sd
from reapy import reascript_api as RPR
from scipy.io.wavfile import write

from logger import setup_logger

AUTOSAVE_INTERVAL = 5

logging = setup_logger("Plugin renderer")
df = pd.DataFrame()


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--mode",
        dest="value_generation_mode",
        type=str,
        default="preset",
        help="Select preset generation mode. If set to 'preset', iterate through available presets; if set to 'random', generate random values for each parameter. Default: 'preset'.",
    )

    parser.add_argument(
        "-i",
        "--iterations",
        dest="no_iterations",
        type=int,
        default=1,
        help="Specify the number of random batches of parameter values to generate. This option is only available when --mode is set to 'random'. Default: 1.",
    )

    parser.add_argument(
        "-d",
        "--device_id",
        dest="device_id",
        type=int,
        default=0,
        help="Specify Blackhole as the audio input device. Default: 0.",
    )

    parser.add_argument(
        "-f",
        "--folder",
        dest="folder",
        type=str,
        default="d",
        help="Name of the subfolder to store rendered presets. Default: 'data'",
    )

    parser.add_argument(
        "-n",
        "--dataset_filename",
        dest="dataset_filename",
        type=str,
        default="dataset",
        help="Set the name of .csv, containing the values of rendered presets. Default: 'dataset'.",
    )

    parser.add_argument(
        "-s", "--samplerate", dest="samplerate", type=int, default=48000, help="Set sampling rate. Default: 48000"
    )

    parser.add_argument(
        "-b", "--blocksize", dest="blocksize", type=int, default=1024, help="Set blocksize in samples. Default: 1024."
    )

    parser.add_argument(
        "-t",
        "--silence_thresh",
        dest="silence_thresh",
        type=float,
        default=1e-6,
        help="Adjust the silence threshold to prevent the recording of silent audio files. Default: 1e-6.",
    )

    args = parser.parse_args()

    try:
        if args.value_generation_mode not in ["preset", "random"]:
            raise ValueError("Invalid mode. Mode should be either 'preset' or 'random'.")
        if args.value_generation_mode == "preset" and args.no_iterations != 1:
            raise ValueError("Iterations argument is only available if mode is set to 'random'.")
        if args.value_generation_mode == "random" and args.no_iterations < 1:
            raise ValueError("The number of parameters batches to be generated must be at least 1.")
    except ValueError as e:
        logging.error(str(e))
        exit(1)

    return args


class Recorder:
    def __init__(self, device_id, samplerate, blocksize, silence_thresh, folder):
        self.device_id = device_id
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.silence_thresh = silence_thresh
        self.folder = folder

        self.stream = None
        self.recording = np.empty((0, 2), dtype=np.float32)

        # create directory and sudirectory if they do not exist
        self.filepath = os.path.join("audio", self.folder)
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)

    def callback(self, indata, frames, time, status):
        self.recording = np.concatenate((self.recording, indata), axis=0)

    def is_silent(self):
        energy = np.sum(self.recording**2)
        return energy < self.silence_thresh

    def start_recording(self):
        logging.info("Recording starts...")
        self.recording = np.empty((0, 2), dtype=np.float32)
        self.stream = sd.InputStream(
            callback=self.callback,
            channels=2,
            samplerate=self.samplerate,
            device=self.device_id,
            blocksize=self.blocksize,
        )
        self.stream.start()

    def stop_recording(self):
        if self.stream is not None:
            logging.info("Record stops.")
            self.stream.stop()
            self.stream.close()
            self.stream = None

            if not self.is_silent():
                # generate a timestamp for filename
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}.wav"
                full_path = os.path.join(self.filepath, filename)
                logging.info(f"Writing audio at {full_path}")
                write(full_path, self.samplerate, self.recording)

                # return filename for use in main()
                return filename
            else:
                logging.info(f"Silence detected, nothing to save on disk!")

        if self.stream is None:
            logging.info("No active stream to stop.")


def save_to_csv(df, name):
    # create data folder if it does not exist
    if not os.path.exists("data"):
        os.makedirs("data")

    # generate a timestamp for file name
    filepath = f"rendered_presets_{name}.csv"

    # check if file already exists
    file_exists = os.path.isfile(os.path.join("data", filepath))

    # append dataframe to csv file
    df.to_csv(os.path.join("data", filepath), mode="a", header=not file_exists, index=False)


def signal_handler(sig, frame):
    global df
    args = get_arguments()

    logging.info(f"Abort process and save dataframe...")
    dataset_filename = args.dataset_filename

    save_to_csv(df, dataset_filename)
    exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    args = get_arguments()
    mode = args.value_generation_mode
    no_iterations = args.no_iterations
    device_id = args.device_id
    folder = args.folder
    dataset_filename = args.dataset_filename
    samplerate = args.samplerate
    blocksize = args.blocksize
    silence_thresh = args.silence_thresh

    # Link and get current project
    reapy.connect()
    project = reapy.Project()

    # Get track and plugin
    track = project.tracks[0]
    plugin = track.fxs[0]

    # Create an instance of Dataframe and Recorder
    global df
    recorder = Recorder(device_id, samplerate, blocksize, silence_thresh, folder)

    # preset mode: use if factory presets are available
    if mode == "preset":
        # Get preset no. and set it to 0 to start from there
        num_presets = plugin.n_presets
        plugin.preset = 0

        # init an empty dataframe to store the values at each iteration
        df = pd.DataFrame()

        for i in range(num_presets):
            print(f"n preset: {i}")
            plugin.preset = i
            name = plugin.preset

            # init a dict to store parameters values
            param_values = {"name": name}
            logging.info(f"Preset: {name}")

            # get and log all parameters' values for the current preset
            for j in range(plugin.n_params):
                param = plugin.params[j]
                param_value = RPR.TrackFX_GetParam(track.id, plugin.index, j, 0.0, 1.0)
                param_values[param.name] = param_value[0]
                logging.info(f"Parameter {j}: {param.name}, Value: {param_value[0]}")  # get only current value

            project.cursor_position = 0

            RPR.CSurf_OnPlay()
            recorder.start_recording()

            time.sleep(2)

            RPR.CSurf_OnStop()
            filename = recorder.stop_recording()

            param_values["file"] = filename
            df = pd.concat([df, pd.DataFrame([param_values])], ignore_index=True)

            if (i + 1) % AUTOSAVE_INTERVAL == 0:
                save_to_csv(df, dataset_filename)
                # init an empty dataframe to store a new batch of values once you saved it to a disk
                df = pd.DataFrame()

        # call save_to_csv to save data if n_iterations is not a multiple of AUTOSAVE_INTERVAL
        save_to_csv(df, dataset_filename)

    # random mode: use to generate random preset values if factory presets are not available
    elif mode == "random":
        # init an empty dataframe to store the values at each iteration
        df = pd.DataFrame()

        for _ in range(no_iterations):
            param_values = {}

            for j in range(plugin.n_params):
                param = plugin.params[j]
                random_value = random.uniform(0.0, 1.0)
                RPR.TrackFX_SetParam(track.id, plugin.index, j, random_value)
                param_values[param.name] = random_value
                logging.info(f"Parameter {j}: {param.name}, Value: {random_value}")

            project.cursor_position = 0

            RPR.CSurf_OnPlay()
            recorder.start_recording()

            time.sleep(2)

            RPR.CSurf_OnStop()
            filename = recorder.stop_recording()

            # if the recording is not silent, add a new row to the df
            if filename is not None:
                param_values["name"] = "name_" + filename.replace(".wav", "")
                param_values["file"] = filename
                df = pd.concat([df, pd.DataFrame([param_values])], ignore_index=True)

                # autosave each 5 rendered presets
                if (i + 1) % AUTOSAVE_INTERVAL == 0:
                    save_to_csv(df, dataset_filename)
                    # init an empty dataframe to store a new batch of values once you saved it to a disk
                    df = pd.DataFrame()

        # call save_to_csv to save data if n_iterations is not a multiple of AUTOSAVE_INTERVAL
        save_to_csv(df, dataset_filename)


if __name__ == "__main__":
    main()

# TODO:
# 1. use reapy.inside_reaper()
# 2. make multithread (queue + threading)
# 3. set time.sleep(1)
