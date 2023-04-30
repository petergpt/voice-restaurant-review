import tempfile
import base64
import os


def save_voice_recording(audio_bytes, duration):
    return audio_bytes, duration
    temp_file.write(audio_bytes)
    temp_file.close()

    with open(temp_file.name, "rb") as wav_file:
        wav_data = wav_file.read()

    os.unlink(temp_file.name)

    return base64.b64encode(wav_data).decode("utf-8"), duration