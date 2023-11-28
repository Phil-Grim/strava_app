import strava
import streamlit as st

st.set_page_config(
    page_title="Streamlit Activity Viewer for Strava",
    page_icon=":circus_tent:",
)

strava_header = strava.header()
