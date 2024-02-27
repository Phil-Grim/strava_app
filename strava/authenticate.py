import streamlit as st
import httpx
import base64

from strava.constants import *


def header():
    '''adds 3 columns to the page, along with an empty container in the 3rd column'''
    col1, col2, col3 = st.columns(3)

    with col3:
        strava_button = st.empty()

    return col1, col2, col3, strava_button


@st.cache(show_spinner=False)
def load_image_as_base64(image_path):
    with open(image_path, "rb") as f:
        contents = f.read()
    return base64.b64encode(contents).decode("utf-8")


def powered_by_strava_logo():
    base64_image = load_image_as_base64("./static/api_logo_pwrdBy_strava_horiz_light.png")
    st.markdown(
        f'<img src="data:image/png;base64,{base64_image}" width="100%" alt="powered by strava">',
        unsafe_allow_html=True,
    )

@st.cache_data(show_spinner=False)
def authorization_url():
    request = httpx.Request(
        method="GET",
        url=STRAVA_AUTHORIZATION_URL,
        params={
            "client_id": STRAVA_CLIENT_ID,
            "redirect_uri": APP_URL,
            "response_type": "code",
            "approval_prompt": "auto",
            "scope": "activity:read_all"
        }
    )

    return request.url


def login_header(header=None):
    strava_authorization_url = authorization_url()

    if header is None:
        base = st
    else:
        col1, _, _, button = header
        base = button

    with col1:
        # powered_by_strava_logo()
        st.image('static/api_logo_pwrdBy_strava_horiz_light.png')

    base64_image = load_image_as_base64("./static/btn_strava_connectwith_orange@2x.png")
    base.markdown(
        (
            f"<a href=\"{strava_authorization_url}\">"
            f"  <img alt=\"strava login\" src=\"data:image/png;base64,{base64_image}\" width=\"100%\">"
            f"</a>"
        ),
        unsafe_allow_html=True,
    )


def logout_header(strava_auth, header=None):
    if header is None:
        base = st
    else:
        col1, col2, _, button = header
        base = button

    with col1:
        first_name = strava_auth["athlete"]["firstname"]
        last_name = strava_auth["athlete"]["lastname"]
        col1.markdown(f"*Welcome, {first_name} {last_name}!*") 

    with col2:
        powered_by_strava_logo()

    base.markdown(f'''
        <a target="_self" href={APP_URL}><button style="background-color:{STRAVA_ORANGE};">Log Out</button></a>
        ''',
        unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def exchange_authorization_code(authorization_code):
    response = httpx.post(
        url="https://www.strava.com/oauth/token",
        json={
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "code": authorization_code,
            "grant_type": "authorization_code",
        }
    )
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError:
        st.error("Something went wrong while authenticating with Strava. Please reload and try again")
        st.query_params.dict()
        st.stop()
        return

    strava_auth = response.json()

    return strava_auth

# @st.cache_data(show_spinner=False)
def authentication(header=None):
    # query_parameters = st.experimental_get_query_params()
    query_parameters = st.query_params.to_dict()
    try: 
        authorisation_code = query_parameters["code"]
    except:
        authorisation_code = None

    if authorisation_code is None:
        login_header(header=header)
        st.stop()
    else:
        strava_auth = exchange_authorization_code(authorisation_code)
        logout_header(strava_auth, header=header)
        # st.query_params.clear()

    return strava_auth


# @st.cache(show_spinner=False)
# def get_activities(auth,page=1):
#     access_token = auth["access_token"]
#     response = httpx.get(
#         url=f"{STRAVA_API_BASE_URL}/athlete/activities",
#         params ={
#             'per_page':200, 'page':page
#         },
#         headers={
#             "Authorization": f"Bearer {access_token}",
#         },
#     )

#     return response.json()


##### Take Json, add a slider and extract json into a cleaned table 


# import base64
# import os
# import pandas as pd
# import arrow
# import httpx
# import streamlit as st
# from datetime import datetime, timedelta
# from bokeh.models.widgets import Div


# def activities_slider(activities):
#     # using min and max start date from get_activities output (the json of all strava activities for the user) 
#     # min_date = datetime.strptime(activities['start_date'].iloc[0][:10],'%Y-%m-%d')
#     # max_date = datetime.strptime(activities['start_date'].iloc[-1][:10],'%Y-%m-%d')
#     min_date = datetime.date(datetime.strptime(activities[0]['start_date'][:10],'%Y-%m-%d'))
#     max_date = datetime.date(datetime.strptime(activities[-1]['start_date'][:10],'%Y-%m-%d'))
    
#     start_time = st.slider(
#     "Select a date range",
#     min_date,
#     max_date,
#     value=[min_date, max_date],
#     help='Filter your strava activities by date. This will also change the headline statistics'
#     )

#     return start_time

# # Used to add the hyperlink in convert_json_to_df function
# def make_clickable(url, name):
#     return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url,name)

# # functions to format average speed to a minutes / seconds format
# def frac(n):
#     i = int(n)
#     f = round((n - int(n)), 4)
#     return (i, f)

# def frmt(min):
#     minutes, _sec = frac(min)
#     seconds, _msecs = frac(_sec*60)
#     if seconds > 9:
#         return "%s:%s"%(minutes, seconds)
#     else:
#         return "%s:0%s"%(minutes, seconds)


# def convert_json_to_df(activities):
#     date_distance_list = []
#     count = 0
#     for i in activities:
#         if i['sport_type'] == 'Run':
#             activity_url = f"https://www.strava.com/activities/{i['id']}"
#             date_distance_list.append([i['id'], activity_url, i['name'], i['start_date'][:10], i['distance'], i['moving_time'], i['total_elevation_gain'], i['end_latlng'], i['average_speed'], i['max_speed']])
#             try:
#                 date_distance_list[count].append(i['average_heartrate'])
#                 date_distance_list[count].append(i['max_heartrate'])
#             except:
#                 date_distance_list[count].append('None')
#                 date_distance_list[count].append('None')
#             count += 1
            
#     activities_df = pd.DataFrame(date_distance_list, columns = ['ID', 'Link to Activity', 'Name', 'Date', 'Distance', 'Moving Time', 'Elevation Gain (m)', 'End Location', 'Average Speed', 'Max Speed', 'Average HR', 'Max HR'])
#     activities_df.sort_values(by='Date', inplace=True)
#     activities_df['Date'] = pd.to_datetime(activities_df['Date'], format='%Y-%m-%d').dt.date
#     activities_df['Link to Activity - other approach'] = activities_df.apply(lambda x: make_clickable(x['Link to Activity'], x['Link to Activity']), axis=1)
#     activities_df['Distance'] = pd.to_numeric(activities_df['Distance'])
#     activities_df['Distance'] = activities_df['Distance']/1000

#     activities_df['Moving Time (mins)'] = activities_df['Moving Time']/60 # moving time is now in mins
#     activities_df['Average Speed'] = 1/(activities_df['Average Speed']*(60/1000))
#     activities_df['Max Speed'] = 1/(activities_df['Max Speed']*(60/1000))
#     activities_df['Distance (km)'] = activities_df['Distance']

#     # Using above functions to format ave/max speed and moving time
#     formatted_speed = []
#     for index, row in activities_df.iterrows():
#         formatted_speed.append(frmt(row['Average Speed']))
    
#     formatted_max_speed = []
#     for index, row in activities_df.iterrows():
#         formatted_max_speed.append(frmt(row['Max Speed']))
        
#     formatted_moving_time = []
#     for index, row in activities_df.iterrows():
#         formatted_moving_time.append(frmt(row['Moving Time (mins)']))
    
#     activities_df['Average Speed (min/km)'] = formatted_speed
#     activities_df['Max Speed (min/km)'] = formatted_max_speed
#     activities_df['Moving Time (mins)'] = formatted_moving_time

#     activities_df = activities_df[['Name', 'Link to Activity', 'Date', 'Distance (km)', 'Moving Time (mins)', 'Elevation Gain (m)', 'Average Speed (min/km)', 'Max Speed (min/km)', 'Average HR', 'Max HR']]

#     return activities_df

# def filter_activities_from_slider(activities_df, start_time_slider):
#     filtered_df = activities_df.loc[(activities_df['Date'] >= start_time_slider[0]) & (activities_df['Date'] <= start_time_slider[1])]
#     return filtered_df


# def adding_headline_numbers(activities_df):
#     week_distance = round(activities_df['Distance (km)'].sum(), 1)
#     return week_distance
#     # make this recursive








    
