import streamlit as st
import os

APP_URL = "https://stravaapp-5jhpgdn9kfmhmkdy5d5yrs.streamlit.app/"


STRAVA_CLIENT_ID = st.secrets["STRAVA_CLIENT_ID"]
STRAVA_CLIENT_SECRET = st.secrets["STRAVA_CLIENT_SECRET"]


STRAVA_AUTHORIZATION_URL = "https://www.strava.com/oauth/authorize"
STRAVA_API_BASE_URL = "https://www.strava.com/api/v3"
DEFAULT_ACTIVITY_LABEL = "NO_ACTIVITY_SELECTED"
STRAVA_ORANGE = "#fc4c02"