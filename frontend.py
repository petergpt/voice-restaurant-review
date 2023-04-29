import streamlit as st
from audio_recorder_streamlit import audio_recorder
from database import insert_survey_record
from voice_recording import save_voice_recording
from openai_api import transcribe_audio, summarize_text
from datetime import datetime
import uuid

def render_frontend():
    st.title("Quick Customer Surveys")

    audio_bytes = audio_recorder()
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")

        # Save the audio bytes as an MP3 file
        audio_data, duration = save_voice_recording(audio_bytes, 180)  # Assume 3 minutes for now

        # Transcribe and summarize the text
        transcribed_text = transcribe_audio(audio_data)
        summarized_output = summarize_text(transcribed_text)

        # Display the transcribed and summarized text
        st.write("Original Transcription:")
        st.text_area("", transcribed_text, height=100)

        st.write("Summarized Output:")
        edited_output = st.text_area("", summarized_output, height=100)

        if st.button("Submit"):
            user_id = str(uuid.uuid4())  # Generate a random user ID
            insert_survey_record(user_id, datetime.utcnow(), duration, audio_data, transcribed_text, edited_output)
            st.success("Survey submitted successfully!")