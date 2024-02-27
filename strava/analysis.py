# from strava.authenticate import *
from strava.constants import *
import httpx
import streamlit as st

def get_activities(auth,page=1):
    access_token = auth["access_token"]
    response = httpx.get(
        url=f"{STRAVA_API_BASE_URL}/athlete/activities",
        params ={
            'per_page':200, 'page':page
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    return response.json()