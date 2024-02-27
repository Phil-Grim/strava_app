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


@st.cache_data(show_spinner=False)
def activity_stream(refresh_token, activity_id):
    '''Returns stream of distance and time data for a given activity_id'''

    access_token = authenticate.access_from_refresh(refresh_token)
    response = httpx.get(
        url=f"{STRAVA_API_BASE_URL}/activities/{activity_id}/streams?access_token={access_token}",
        params ={
            'keys': ['distance', 'time'], 'keys_by_type': True
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    distance_list = response.json()[0]['data']
    time_list = response.json()[1]['data']
                                       
    speeds_dict = {round(distance_list[i]):time_list[i] for i in range(len(distance_list))}
    activity_distance = list(speeds_dict)[-1]

    return speeds_dict,activity_distance


@st.cache_data(show_spinner=False)
def activity_fastest_km(speeds_dict, activity_distance):
    '''Returns the fastest km split in a given activity'''

    times = []
    for i in range(activity_distance+1):
        try:
            end_time = speeds_dict[i]
            if i-1000 in speeds_dict.keys():
                start_time = speeds_dict[i-1000]
                total_time = end_time - start_time
            elif i-1001 in speeds_dict.keys():
                start_time = speeds_dict[i-1001]
                total_time = end_time - start_time
            elif i-999 in speeds_dict.keys():
                start_time = speeds_dict[i-999]
                total_time = end_time - start_time
            elif i-10012 in speeds_dict.keys():
                start_time = speeds_dict[i-1002]
                total_time = end_time - start_time
            elif i-998 in speeds_dict.keys():
                start_time = speeds_dict[i-998]
                total_time = end_time - start_time    
            times.append(total_time)
        except:
            continue
    return min(times)



