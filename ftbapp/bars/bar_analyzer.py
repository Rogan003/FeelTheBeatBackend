import librosa
import numpy as np
import json

def convert_song_to_bars(y, sr):
    frame_duration = 0.05         # 0.05 seconds per frame = 20 FPS
    n_bars = 45                   # Fewer bars = bigger differences = more punch

    # === Step 1: Calculate hop length ===
    hop_length = int(sr * frame_duration)

    # === Step 2: Extract Mel Spectrogram ===
    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=2048,
        hop_length=hop_length,
        n_mels=n_bars
    )

    # === Step 3: Convert to dB ===
    mel_db = librosa.power_to_db(mel, ref=np.max)

    # === Step 4: Transpose to get list per frame ===
    frames = mel_db.T.tolist()

    # === Step 5: Normalize and boost explosiveness ===
    normalized_frames = []
    for frame in frames:
        clipped = np.clip(frame, -60, 0)
        norm = [(val + 60) / 60 for val in clipped]
        boosted = [v**2 for v in norm]  # Exponential curve for explosive energy
        normalized_frames.append(boosted)

    return normalized_frames