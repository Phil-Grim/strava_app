import httpx
import streamlit as st
import numpy as np

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
            elif i-1002 in speeds_dict.keys():
                start_time = speeds_dict[i-1002]
                total_time = end_time - start_time
            elif i-998 in speeds_dict.keys():
                start_time = speeds_dict[i-998]
                total_time = end_time - start_time    
            times.append(total_time)
        except:
            continue
    if len(times) == 0:
        return np.nan
    else:
        return min(times)
    
@st.cache_data(show_spinner=False)
def activity_fastest_five_km(speeds_dict, activity_distance):
    '''Returns fastest 5 km split in a given activity '''

    times = []
    for i in range(activity_distance+1):
        try:
            end_time = speeds_dict[i]
            if i-5000 in speeds_dict.keys():
                start_time = speeds_dict[i-5000]
                total_time = end_time - start_time
            elif i-5001 in speeds_dict.keys():
                start_time = speeds_dict[i-5001]
                total_time = end_time - start_time
            elif i-4999 in speeds_dict.keys():
                start_time = speeds_dict[i-4999]
                total_time = end_time - start_time
            elif i-5002 in speeds_dict.keys():
                start_time = speeds_dict[i-5002]
                total_time = end_time - start_time
            elif i-4998 in speeds_dict.keys():
                start_time = speeds_dict[i-4998]
                total_time = end_time - start_time    
            times.append(total_time)
        except:
            continue
    if len(times) == 0:
        return np.nan
    else:
        return min(times)

@st.cache_data(show_spinner=False)
def activity_fastest_ten_km(speeds_dict, activity_distance):
    '''Returns fastest 5 km split in a given activity '''

    times = []
    for i in range(activity_distance+1):
        try:
            end_time = speeds_dict[i]
            if i-10000 in speeds_dict.keys():
                start_time = speeds_dict[i-10000]
                total_time = end_time - start_time
            elif i-10001 in speeds_dict.keys():
                start_time = speeds_dict[i-10001]
                total_time = end_time - start_time
            elif i-9999 in speeds_dict.keys():
                start_time = speeds_dict[i-9999]
                total_time = end_time - start_time
            elif i-10002 in speeds_dict.keys():
                start_time = speeds_dict[i-10002]
                total_time = end_time - start_time
            elif i-9998 in speeds_dict.keys():
                start_time = speeds_dict[i-9998]
                total_time = end_time - start_time    
            times.append(total_time)
        except:
            continue
    if len(times) == 0:
        return np.nan
    else:
        return min(times)
    

@st.cache_data(show_spinner=False)
def activity_fastest_half(speeds_dict, activity_distance):
    '''Returns fastest 5 km split in a given activity '''

    times = []
    for i in range(activity_distance+1):
        try:
            end_time = speeds_dict[i]
            if i-21098 in speeds_dict.keys():
                start_time = speeds_dict[i-21098]
                total_time = end_time - start_time
            elif i-21099 in speeds_dict.keys():
                start_time = speeds_dict[i-21099]
                total_time = end_time - start_time
            elif i-21097 in speeds_dict.keys():
                start_time = speeds_dict[i-21097]
                total_time = end_time - start_time
            elif i-21100 in speeds_dict.keys():
                start_time = speeds_dict[i-21100]
                total_time = end_time - start_time
            elif i-21096 in speeds_dict.keys():
                start_time = speeds_dict[i-21096]
                total_time = end_time - start_time    
            times.append(total_time)
        except:
            continue
    if len(times) == 0:
        return np.nan
    else:
        return min(times)
    
@st.cache_data(show_spinner=False)
def activity_fastest_mara(speeds_dict, activity_distance):
    '''Returns fastest 5 km split in a given activity '''

    if activity_distance < 42195:
        return np.nan

    times = []
    for i in range(activity_distance+1):
        try:
            end_time = speeds_dict[i]
            if i-42195 in speeds_dict.keys():
                start_time = speeds_dict[i-42195]
                total_time = end_time - start_time
            elif i-42196 in speeds_dict.keys():
                start_time = speeds_dict[i-42196]
                total_time = end_time - start_time
            elif i-42194 in speeds_dict.keys():
                start_time = speeds_dict[i-42194]
                total_time = end_time - start_time
            elif i-42197 in speeds_dict.keys():
                start_time = speeds_dict[i-42197]
                total_time = end_time - start_time
            elif i-42193 in speeds_dict.keys():
                start_time = speeds_dict[i-42193]
                total_time = end_time - start_time    
            times.append(total_time)
        except:
            continue
    if len(times) == 0:
        return np.nan
    else:
        return min(times)


