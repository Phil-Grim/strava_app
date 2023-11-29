import strava
import streamlit as st

st.set_page_config(
    page_title="Streamlit Activity Viewer for Strava",
    page_icon=":circus_tent:",
)

strava_header = strava.header()

strava_auth = strava.authenticate(header=strava_header, stop_if_unauthenticated=False)

if strava_auth is None:
    st.markdown("Use the **Connect with Strava** button at the top of the screen to login!")
    st.warning('Please login!')
    st.stop # stop the rest of the script running - which requires a non-None strava_auth value

json_activities = strava.get_activities(strava_auth)
st.json(json_activities)

