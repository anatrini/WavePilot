# pylint: disable=no-member, unsubscriptable-object

import datetime
import os
import random
import signal
import time

import numpy as np
import pandas as pd
import reapy
import sounddevice as sd

from constants import NUM_CHANNELS, SAMPLERATE, BLOCKSIZE, AUTOSAVE_INTERVAL, TARGET_dBFS, DATASET_FOLDER, RENDERED_AUDIO_FOLDER, RECORDING_LENGTH
from logger import setup_logger
from reapy import reascript_api as RPR
from scipy.io.wavfile import write



log = setup_logger("Plugin renderer")

class DataHandler:
    """Manages dataframe and CSV operations"""
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.df = pd.DataFrame()
        self.counter = 0
        
    def add_record(self, record):
        """Add record with autosave handling"""
        self.df = pd.concat([self.df, pd.DataFrame([record])], ignore_index=True)
        self.counter += 1
        
        if self.counter % AUTOSAVE_INTERVAL == 0:
            self._save()
            self.df = pd.DataFrame()
            
    def final_save(self):
        """Final dataset save"""
        if not self.df.empty:
            self._save()
            
    def _save(self):
        """Internal save implementation"""
        if not os.path.exists(DATASET_FOLDER):
            os.makedirs(DATASET_FOLDER)
            
        filepath = os.path.join(DATASET_FOLDER, "%s.csv" % self.dataset_name)
        self.df.to_csv(filepath, mode='a', header=not os.path.exists(filepath), index=False)
    

def _handle_interrupt(signum, frame, data_handler):
    log.info("Process interrupted! Saving partial data...")
    data_handler.final_save()
    exit(1)


class AudioRecorder:
    """Handles audio recording operations"""
    def __init__(self, folder, silence_thresh):
        self.folder = folder
        self.silence_thresh = silence_thresh
        self.stream = None
        self.recording = np.empty((0, 2), dtype=np.float32)
        self.device_id = self._select_device()
        
    def _select_device(self):
        """Interactive device selection"""
        devices = sd.query_devices()
        
        print("\n=== Available Audio Devices ===")
        for i, dev in enumerate(devices):
            print("[%d] %s (Inputs: %d)" % (i, dev["name"], dev["max_input_channels"]))
            
        while True:
            try:
                choice = int(input("\nEnter device ID: "))
                if 0 <= choice < len(devices):
                    if devices[choice]["max_input_channels"] > 0:
                        log.info("Selected device: %s", devices[choice]["name"])
                        return choice
                    print("Error: Device has no inputs!")
                else:
                    print("Error: Invalid ID!")
            except ValueError:
                print("Error: Numbers only!")

    def _is_silent(self):
        """Check recording energy"""
        return np.sum(self.recording**2) < self.silence_thresh
        
    def start_recording(self):
        """Start audio capture"""
        self.recording = np.empty((0, 2), dtype=np.float32)
        self.stream = sd.InputStream(
            device=self.device_id,
            channels=NUM_CHANNELS,
            samplerate=SAMPLERATE,
            blocksize=BLOCKSIZE,
            callback=self._audio_callback
        )
        self.stream.start()
        
    def stop_recording(self):
        """Stop and save recording"""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            
        if not self._is_silent():
            normalized_audio = self._normalize_audio(self.recording)

            os.makedirs(os.path.join(RENDERED_AUDIO_FOLDER, self.folder), exist_ok=True)
            filename = "%s.wav" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            full_path = os.path.join(RENDERED_AUDIO_FOLDER, self.folder, filename)
            write(full_path, SAMPLERATE, normalized_audio)
            return filename
        return None
    
    def _normalize_audio(self, audio_data):
        if audio_data.size == 0:
            return audio_data
        
        # Estimate peak value
        peak = np.max(np.abs(audio_data))
        if peak == 0:
            return audio_data # prevent division by 0
        
        # Estimate scale factor for target dBFS
        target_linear = 10 ** (TARGET_dBFS / 20)
        scale_factor = target_linear / peak

        # Apply normalization with clipping prevention
        return np.clip(audio_data * scale_factor, -1.0, 1.0)
        
    def _audio_callback(self, indata, frames, time, status):
        """Sounddevice callback"""
        self.recording = np.concatenate((self.recording, indata))

# ======================
# MAIN FUNCTION (LAST)
# ======================

def main(render_mode, 
        directory, 
        dataset_filename, 
        silence_thresh,
        no_iterations):
    
    """Primary entry point for rendering operations"""
    # Initialize core components
    data_handler = DataHandler(dataset_filename)
    recorder = AudioRecorder(directory, silence_thresh)
    
    # REAPER connection
    reapy.connect()
    project = reapy.Project()
    track = project.tracks[0]
    plugin = track.fxs[0]

    signal.signal(signal.SIGINT, lambda s, f: _handle_interrupt(s, f, data_handler))
    
    try:
        # Preset mode logic
        if render_mode == "preset":
            num_presets = plugin.n_presets
            for preset_idx in range(num_presets):
                plugin.preset = preset_idx
                param_values = {"name": plugin.preset}
                
                # Get parameters
                for param_idx in range(plugin.n_params):
                    param = plugin.params[param_idx]
                    value = RPR.TrackFX_GetParam(track.id, plugin.index, param_idx, 0.0, 1.0)[0]
                    param_values[param.name] = value
                    log.info("Parameter %d: %s, Value: %s", 
                            param_idx, param.name, value)
                
                # Record audio
                track.project.cursor_position = 0
                RPR.CSurf_OnPlay()
                recorder.start_recording()
                time.sleep(RECORDING_LENGTH)
                RPR.CSurf_OnStop()
                filename = recorder.stop_recording()
                
                # Save data
                if filename:
                    param_values["file"] = filename
                    data_handler.add_record(param_values)
        
        # Random mode logic        
        else:
            for _ in range(no_iterations):
                param_values = {}
                
                # Generate parameters
                for param_idx in range(plugin.n_params):
                    param = plugin.params[param_idx]
                    rand_val = random.uniform(0.0, 1.0)
                    RPR.TrackFX_SetParam(track.id, plugin.index, param_idx, rand_val)
                    param_values[param.name] = rand_val
                    log.info("Parameter %d: %s, Value: %s", 
                            param_idx, param.name, rand_val)
                
                # Record audio
                track.project.cursor_position = 0
                RPR.CSurf_OnPlay()
                recorder.start_recording()
                time.sleep(RECORDING_LENGTH)
                RPR.CSurf_OnStop()
                filename = recorder.stop_recording()
                
                # Save data
                if filename:
                    param_values.update({
                        "name": "random_%s" % filename.replace(".wav", ""),
                        "file": filename
                    })
                    data_handler.add_record(param_values)
                    
    finally:
        data_handler.final_save()
        recorder.stop_recording()