import subprocess
import json


FFPROBE_PATH = r"C:\Users\dell\Downloads\ffmpeg-9.0.2-essentials_build\ffmpeg-9.0.2-essentials_build\bin\ffprobe.exe"


def get_metadata(filepath):

    command = [
        FFPROBE_PATH,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        filepath
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {
            "error": "Unable to read audio metadata"
        }

    data = json.loads(result.stdout)

    format_data = data.get("format", {})
    streams = data.get("streams", [])

    audio_stream = None

    for stream in streams:
        if stream.get("codec_type") == "audio":
            audio_stream = stream
            break

    if audio_stream is None:
        return {
            "error": "No audio stream found"
        }

    duration = float(
        audio_stream.get(
            "duration",
            format_data.get("duration", 0)
        )
    )

    sample_rate = audio_stream.get(
        "sample_rate",
        "Unknown"
    )

    channels = audio_stream.get(
        "channels",
        "Unknown"
    )

    bitrate = audio_stream.get(
        "bit_rate",
        format_data.get("bit_rate", "Unknown")
    )

    codec = audio_stream.get(
        "codec_name",
        "Unknown"
    )

    codec_long = audio_stream.get(
        "codec_long_name",
        "Unknown"
    )

    format_name = format_data.get(
        "format_name",
        "Unknown"
    )

    return {
        "format": format_name,
        "codec": codec,
        "codec_long": codec_long,
        "duration": round(duration, 2),
        "sample_rate": sample_rate,
        "channels": channels,
        "bitrate": bitrate
    }