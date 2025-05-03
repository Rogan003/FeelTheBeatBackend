from django.core.files.storage import default_storage
from tensorflow.keras import layers, models
import librosa
import numpy as np
import tensorflow as tf
from ftbapp.shared import utils

def extract_mfcc_per_second(y, sr):
    duration = int(librosa.get_duration(y=y, sr=sr))
    mfccs = []
    for sec in range(duration):
        segment = y[sec * sr: (sec + 1) * sr]
        if len(segment) < sr:
            continue
        mfcc = librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=40)
        mfcc_mean = np.mean(mfcc, axis=1)
        mfccs.append(mfcc_mean)
    return np.stack(mfccs)

def predict_colors(model, y, sr):
    mfcc_seq = extract_mfcc_per_second(y, sr)
    input_tensor = np.expand_dims(mfcc_seq, axis=0)  # Shape: (1, time, mfcc_dim)
    rgb_seq = model.predict(input_tensor)[0]
    rgb_scaled = (rgb_seq * 255).astype(int)
    return rgb_scaled.tolist()

def get_colors(file_path):
    model = tf.keras.models.load_model("audio_to_color_model.keras")

    with default_storage.open(file_path, 'rb') as f:
        y, sr = utils.audio_file_to_y_sr(f)

    return predict_colors(model, y, sr)