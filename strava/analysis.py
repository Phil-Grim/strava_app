import httpx
import streamlit as st
import numpy as np
from datetime import datetime
import pandas as pd

from strava import authenticate
from strava.constants import *



@st.cache_data(show_spinner=False)
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


@st.cache_data(show_spinner=False)
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
def get_activities(refresh_token,total_runs, page=1):
    '''Extracts one page of activities (200 activities)
        The total_runs argument ensures that the function is run (and the cached result isn't returned) if another run
        has been added to strava'''
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


def full_activity_list(refresh_token):
    # extracts the full list of activities for every page of activities
    id = athlete_id(refresh_token)

    total_runs = number_of_runs(refresh_token, id) 
    num_pages = int(total_runs/200) + 1
    activities = []
    for i in range(num_pages):
        page = i + 1
        page_activities = get_activities(refresh_token, total_runs, page)
        activities.extend(page_activities)
    return activities


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

    if activity_distance < 1000:
        return np.nan

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

    if activity_distance < 5000:
        return np.nan    

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

    if activity_distance < 10000:
        return np.nan

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

    if activity_distance < 21098:
        return np.nan

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
    

def convertSecs(seconds):
    '''Converting fastest times into a clearer format (from seconds to %H:%M:%S)'''
    if np.isnan(seconds):
        return 'N/A'
    else:
        remaining_seconds = int(seconds) % 60
        minutes = int((seconds/60) % 60)
        hours = int(seconds/(60*60))
        return f'{hours:02d}:{minutes:02d}:{remaining_seconds:02d}'


def activities_slider(activities):
    '''using min and max start date from get_activities output'''

    min_date = datetime.date(datetime.strptime(activities[0]['start_date'][:10],'%Y-%m-%d'))
    max_date = datetime.date(datetime.strptime(activities[-1]['start_date'][:10],'%Y-%m-%d'))
    
    start_time = st.slider(
    "Select a date range",
    min_date,
    max_date,
    value=[min_date, max_date],
    help='Filter your strava activities by date. This will also change the headline statistics'
    )

    return start_time


def filter_activities_from_slider(activities_df, start_time_slider):
    '''filter the resulting dataframe based on a date slider'''
    filtered_df = activities_df.loc[(activities_df['date'] >= start_time_slider[0]) & (activities_df['date'] <= start_time_slider[1])]
    return filtered_df

@st.cache_data(show_spinner=False)
def create_dataframe(activities, refresh_token):
    with st.spinner(f"Generating fastes splits for Strava actvities"):
        rows = []
        for i in activities[:30]:
            activity_id = i["id"]
            name = i["name"]
            kms = round(i["distance"] / 1000, 2)
            dates = i["start_date"][:10]

            stream = activity_stream(refresh_token, activity_id)

            fastest_km_time = activity_fastest_km(stream[0], stream[1])
            fastest_five_km_time = activity_fastest_five_km(stream[0], stream[1])
            fastest_ten_km_time = activity_fastest_ten_km(stream[0], stream[1])
            fastest_half_time = activity_fastest_half(stream[0], stream[1])
            fastest_mara_time = activity_fastest_mara(stream[0], stream[1])

            rows.append([str(activity_id), name, dates, kms, fastest_km_time, fastest_five_km_time, fastest_ten_km_time, fastest_half_time, fastest_mara_time])

        df = pd.DataFrame(rows, columns=['activity_id', 'name', 'date', 'kms', '1km', '5km', '10km', 'Half', 'Marathon'])
        df[['1km', '5km', '10km', 'Half', 'Marathon']] = df[['1km', '5km', '10km', 'Half', 'Marathon']].applymap(convertSecs)
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d').dt.date
        return df 
