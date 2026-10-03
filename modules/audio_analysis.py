import matplotlib

matplotlib.use("Agg")

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
import tempfile


FFMPEG_PATH = r"C:\Users\dell\Downloads\ffmpeg-9.0.2-essentials_build\ffmpeg-9.0.2-essentials_build\bin\ffmpeg.exe"


def analyze_audio(filepath, output_folder):

    # -------------------------
    # Convert audio to WAV using FFmpeg
    # -------------------------

    temp_wav = os.path.join(
        tempfile.gettempdir(),
        "audiotrace_temp.wav"
    )

    command = [
        FFMPEG_PATH,
        "-y",
        "-i",
        filepath,
        "-ar",
        "48000",
        "-ac",
        "1",
        temp_wav
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(
            "FFmpeg could not convert the audio file."
        )

    # -------------------------
    # Load converted WAV file
    # -------------------------

    y, sr = librosa.load(
        temp_wav,
        sr=None,
        mono=True
    )

    # Create output folder
    os.makedirs(
        output_folder,
        exist_ok=True
    )

    # -------------------------
    # 1. Waveform
    # -------------------------

    plt.figure(figsize=(10, 4))

    librosa.display.waveshow(
        y,
        sr=sr
    )

    plt.title("Audio Waveform")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")

    waveform_path = os.path.join(
        output_folder,
        "waveform.png"
    )

    plt.savefig(
        waveform_path,
        bbox_inches="tight"
    )

    plt.close()

    # -------------------------
    # 2. Spectrogram
    # -------------------------

    D = librosa.stft(y)

    spectrogram = librosa.amplitude_to_db(
        np.abs(D),
        ref=np.max
    )

    plt.figure(figsize=(10, 4))

    librosa.display.specshow(
        spectrogram,
        sr=sr,
        x_axis="time",
        y_axis="hz"
    )

    plt.colorbar(
        format="%+2.0f dB"
    )

    plt.title("Audio Spectrogram")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Frequency (Hz)")

    spectrogram_path = os.path.join(
        output_folder,
        "spectrogram.png"
    )

    plt.savefig(
        spectrogram_path,
        bbox_inches="tight"
    )

    plt.close()

    # -------------------------
    # 3. RMS Energy
    # -------------------------

    rms = librosa.feature.rms(
        y=y
    )[0]

    average_rms = float(
        np.mean(rms)
    )

    maximum_rms = float(
        np.max(rms)
    )

    # -------------------------
    # 4. Zero Crossing Rate
    # -------------------------

    zcr = librosa.feature.zero_crossing_rate(
        y
    )[0]

    average_zcr = float(
        np.mean(zcr)
    )

    # -------------------------
    # 5. Frequency Analysis using FFT
    # -------------------------

    # Perform Fast Fourier Transform
    fft_result = np.fft.rfft(y)

    # Calculate magnitude
    magnitude = np.abs(
        fft_result
    )

    # Generate frequency values
    frequencies = np.fft.rfftfreq(
        len(y),
        d=1 / sr
    )

    # Find dominant frequency
    dominant_index = np.argmax(
        magnitude
    )

    dominant_frequency = frequencies[
        dominant_index
    ]

    # -------------------------
    # Create Frequency Spectrum
    # -------------------------

    plt.figure(figsize=(10, 4))

    plt.plot(
        frequencies,
        magnitude
    )

    plt.title(
        "Frequency Spectrum (FFT)"
    )

    plt.xlabel(
        "Frequency (Hz)"
    )

    plt.ylabel(
        "Magnitude"
    )

    # Display frequencies up to 20 kHz
    plt.xlim(
        0,
        20000
    )

    frequency_path = os.path.join(
        output_folder,
        "frequency_spectrum.png"
    )

    plt.savefig(
        frequency_path,
        bbox_inches="tight"
    )

    plt.close()

    # -------------------------
    # Return results
    # -------------------------

    return {

        "waveform": waveform_path,

        "spectrogram": spectrogram_path,

        "frequency_spectrum": frequency_path,

        "dominant_frequency": round(
            float(dominant_frequency),
            2
        ),

        "average_rms": round(
            average_rms,
            4
        ),

        "maximum_rms": round(
            maximum_rms,
            4
        ),

        "average_zcr": round(
            average_zcr,
            4
        ),

        "sample_rate": sr
    }