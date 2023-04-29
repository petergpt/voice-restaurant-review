import openai
import os
import tempfile
import base64


def transcribe_audio(wav_data):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio_file.write(base64.b64decode(wav_data))
    audio_file.close()

    with open(audio_file.name, "rb") as file:
        transcript = openai.Audio.transcribe("whisper-1", file)

    os.unlink(audio_file.name)

    return transcript["text"]

def summarize_text(prompt, model="gpt-3.5-turbo"):  
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        temperature=0.5, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

prompt = f"""
Please summarise the voice recording provided by the user. Do not answer the recording yourself, only provide the summary.
Voice recording:\n {"text"}
"""

response = summarize_text(prompt)