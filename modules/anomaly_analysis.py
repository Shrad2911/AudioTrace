import librosa
import numpy as np
import subprocess
import tempfile
import os


FFMPEG_PATH = r"C:\Users\dell\Downloads\ffmpeg-9.0.2-essentials_build\ffmpeg-9.0.2-essentials_build\bin\ffmpeg.exe"


def analyze_anomalies(filepath):

    # -------------------------
    # Convert audio to WAV
    # -------------------------

    temp_wav = os.path.join(
        tempfile.gettempdir(),
        "audiotrace_anomaly.wav"
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
    # Load audio
    # -------------------------

    y, sr = librosa.load(
        temp_wav,
        sr=None,
        mono=True
    )

    # -------------------------
    # RMS Energy
    # -------------------------

    rms = librosa.feature.rms(
        y=y
    )[0]

    average_rms = np.mean(rms)

    # -------------------------
    # Silence Detection
    # -------------------------

    silence_threshold = average_rms * 0.1

    silent_frames = rms < silence_threshold

    silence_percentage = (
        np.sum(silent_frames) / len(rms)
    ) * 100

    # -------------------------
    # Energy Variation
    # -------------------------

    rms_std = np.std(rms)

    energy_variation = (
        rms_std / average_rms
        if average_rms > 0
        else 0
    )

    # -------------------------
    # Sudden Signal Changes
    # -------------------------

    rms_difference = np.abs(
        np.diff(rms)
    )

    if len(rms_difference) > 0:

        sudden_change_threshold = (
            np.mean(rms_difference)
            + 3 * np.std(rms_difference)
        )

        sudden_changes = np.sum(
            rms_difference > sudden_change_threshold
        )

    else:
        sudden_changes = 0

    # -------------------------
    # Generate Findings
    # -------------------------

    findings = []

    # Silence finding
    if silence_percentage > 30:

        findings.append(
            "High amount of low-energy/silent regions detected."
        )

    else:

        findings.append(
            "No unusually high amount of silence detected."
        )

    # Energy variation finding
    if energy_variation > 1.0:

        findings.append(
            "High variation in signal energy detected."
        )

    else:

        findings.append(
            "Signal energy variation is within the observed range."
        )

    # Sudden change finding
    if sudden_changes > 10:

        findings.append(
            "Multiple sudden signal transitions detected."
        )

    else:

        findings.append(
            "No unusually high number of sudden signal transitions detected."
        )

    # -------------------------
    # Return Results
    # -------------------------

    return {

        "silence_percentage": round(
            float(silence_percentage),
            2
        ),

        "energy_variation": round(
            float(energy_variation),
            2
        ),

        "sudden_changes": int(
            sudden_changes
        ),

        "findings": findings
    }