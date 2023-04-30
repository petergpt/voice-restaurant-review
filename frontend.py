import streamlit as st
from database import insert_survey_record, get_survey_records, create_surveys_table
from voice_recording import save_voice_recording
from openai_api import transcribe_audio, summarize_text
from audio_recorder_streamlit import audio_recorder
import uuid
from datetime import datetime
import io
import wave

def get_audio_duration(audio_bytes):
    with io.BytesIO(audio_bytes) as audio_file:
        with wave.open(audio_file, "rb") as wave_file:
            frame_rate = wave_file.getframerate()
            n_frames = wave_file.getnframes()
            duration = n_frames / float(frame_rate)
    return duration

def render_frontend():
    create_surveys_table()

    st.title("Voice Restaurant Reviews")

    user_id = str(uuid.uuid4())

    st.write("Tell us what you thought in your own voice:")
    audio_bytes = audio_recorder(
        text="Click to Record",
        recording_color="#e8b62c",
        neutral_color="#6aa36f",
        icon_name="microphone",
        icon_size="2x",
        pause_threshold=None,
        energy_threshold=(3000, 3000),
    )

    if audio_bytes:
        duration = get_audio_duration(audio_bytes)

        if duration < 1:
            st.warning("The recording is too short. Please record again.")
        else:
            st.audio(audio_bytes, format="audio/wav")
            recording_length = 180  # Assume 3 minutes for now

            with st.spinner("Saving voice recording..."):
                wav_data, duration = save_voice_recording(audio_bytes, recording_length)

            with st.spinner("Transcribing voice input..."):
                transcribed_text = transcribe_audio(wav_data)

            with st.spinner("Summarizing transcribed text..."):
                summarized_output = summarize_text(transcribed_text)

            st.write("Original Transcription:")
            st.text_area("", transcribed_text, height=100)

            st.write("Summarized Output:")
            edited_output = st.text_area("", summarized_output, height=100)

            if st.button("Submit"):
                insert_survey_record(user_id, datetime.utcnow(), duration, wav_data, transcribed_text, edited_output)
                st.success("Survey submitted successfully!")

    st.markdown("---")
    st.subheader("Previous Surveys")
    records = get_survey_records(user_id)
    for record in records:
        st.write(f"Submitted at: {record['recording_time']}")
        st.write(f"Duration: {record['recording_length']} seconds")
        st.write(f"Original Transcription: {record['transcribed_wav']}")
        st.write(f"Summarized Output: {record['summarized_output']}")
        st.markdown("---")