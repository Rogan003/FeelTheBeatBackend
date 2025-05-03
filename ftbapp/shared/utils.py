import io
import librosa


def audio_file_to_y_sr(audio_file):
    # Use librosa to load the audio data and sample rate
    y, sr = librosa.load(audio_file, sr=None)

    return y, sr
