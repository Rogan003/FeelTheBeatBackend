import librosa
import numpy as np

def sound_to_vibration(y, sr):
    DURATION_VIBRATION = 0.1  # Trajanje vibracije po beatu (u sekundama, npr. 100ms)

    # 2. Detect beats
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # 3. convert beat frames to time
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # 4. calculating vibration intensity
    vibration_times = []
    vibration_intensities = []

    samples_per_vibration = int(DURATION_VIBRATION * sr)

    for beat_time in beat_times:
        beat_sample = int(beat_time * sr)

        start_sample = max(0, beat_sample - samples_per_vibration // 2)
        end_sample = min(len(y), beat_sample + samples_per_vibration // 2)

        segment = y[start_sample:end_sample]

        if len(segment) > 0:
            rms = np.sqrt(np.mean(segment ** 2))
            vibration_times.append(beat_time)
            vibration_intensities.append(rms)

    # 5. Normalize vibration intensities
    vibration_intensities = np.array(vibration_intensities)
    vibration_intensities = (vibration_intensities - np.min(vibration_intensities)) / (np.max(vibration_intensities) - np.min(vibration_intensities))  # Normalizacija na opseg [0, 1]
    vibration_intensities = (vibration_intensities * 255).astype(np.uint8)

    return vibration_times, vibration_intensities

