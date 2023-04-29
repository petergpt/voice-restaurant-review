import streamlit as st
from frontend import render_frontend

def main():
    st.set_page_config(
        page_title="Quick Customer Surveys",
        page_icon=":speech_balloon:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    render_frontend()

if __name__ == "__main__":
    main()