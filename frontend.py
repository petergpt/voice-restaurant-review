import streamlit as st
from database import insert_survey_record, get_survey_records, create_surveys_table
from voice_recording import save_voice_recording
from openai_api import transcribe_audio, summarize_text
from audio_recorder_streamlit import audio_recorder
import uuid
from datetime import datetime

def apply_custom_css():
    custom_css = """
        <style>
            .recorder-container .ar-button-container {
                height: 60px !important;
            }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def render_frontend():
    create_surveys_table()
    apply_custom_css()

    st.title("Quick Customer Surveys")

    user_id = str(uuid.uuid4())

    st.write("Record your voice (up to 3 minutes):")
    with st.container() as recorder_container:
        st.write('<div class="recorder-container"></div>', unsafe_allow_html=True)
        audio_bytes = audio_recorder(
            text="Click to Record",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_name="microphone",
            icon_size="2x",
            pause_threshold=None,
            energy_threshold=None,
        )

    if audio_bytes:
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