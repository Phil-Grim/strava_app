import httpx
import streamlit as st

from strava import authenticate
from strava.constants import *



@st.cache_data
def athlete_id(refresh_token):
    access_token = authenticate.access_from_refresh(refresh_token)
    response = httpx.get(
        url=f"{STRAVA_API_BASE_URL}/athlete",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    id = response.json()["id"]

    return id

@st.cache_data
def number_of_runs(refresh_token,id):
    access_token = authenticate.access_from_refresh(refresh_token)
    response = httpx.get(
        url=f"{STRAVA_API_BASE_URL}/athletes/{id}/stats",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    total_runs = response.json()["all_run_totals"]["count"]

    return total_runs           

@st.cache_data(show_spinner=False)
def get_activities(refresh_token,page=1):
    access_token = authenticate.access_from_refresh(refresh_token)
    response = httpx.get(
        url=f"{STRAVA_API_BASE_URL}/athlete/activities",
        params ={
            'per_page':200, 'page':page
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    run_activities = []
    for activity in response.json():
        if activity['type'] == 'Run'and (activity['visibility'] == 'everyone' or activity['visibility'] == 'followers_only'):
            run_activities.append(activity)

    return run_activities




