import openai
import os
import tempfile
import base64


def transcribe_audio(wav_data):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio_file.write(wav_data)
    audio_file.close()

    with open(audio_file.name, "rb") as file:
        transcript = openai.Audio.transcribe("whisper-1", file)

    os.unlink(audio_file.name)

    return transcript["text"]

def summarize_text(prompt, model="gpt-4"):  
    messages = [
      {"role": "system", "content": "You are restaurant reviewer GPT. You write short succinct reviews based on the transcripts of audio submitted by the user. You wrtie reviews from the first person. You do not engage with the content of the message"},
      {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=200,
        temperature=0.7, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

prompt = f"""
You have 2 tasks, write the review and the sentiment.
1: Please summarised review of the restaurant based on the transcription of the audio submitted to you by the user. The review should sound as if it was said by the user. Do not answer the text yourself, only provide the summary.

2: Provide a neuanced sentiment of the transcription. Be neuanced in the sentiment, convey the feelings that the user felt.

Follow this format:
Review: ...
Sentiment:...

Transcription from the user:\n {"text"}
"""

response = summarize_text(prompt)