import base64
import os

import arrow
import httpx
import streamlit as st
from bokeh.models.widgets import Div

APP_URL = "https://stravaapp-5jhpgdn9kfmhmkdy5d5yrs.streamlit.app/"
STRAVA_CLIENT_ID = "106698"
STRAVA_CLIENT_SECRET = "a66bb23d9597d2b4027ff22a73720f226d021f68"
STRAVA_AUTHORIZATION_URL = "https://www.strava.com/oauth/authorize"
STRAVA_API_BASE_URL = "https://www.strava.com/api/v3"
DEFAULT_ACTIVITY_LABEL = "NO_ACTIVITY_SELECTED"


def header():
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
        powered_by_strava_logo()

    base64_image = load_image_as_base64("./static/btn_strava_connectwith_orange@2x.png")
    base.markdown(
        (
            f"<a href=\"{strava_authorization_url}\">"
            f"  <img alt=\"strava login\" src=\"data:image/png;base64,{base64_image}\" width=\"100%\">"
            f"</a>"
        ),
        unsafe_allow_html=True,
    )

def logout_header(header=None):
    if header is None:
        base = st
    else:
        _, col2, _, button = header
        base = button


    with col2:
        powered_by_strava_logo()

    if base.button("Log out"):
        js = f"window.location.href = '{APP_URL}'"
        html = f"<img src onerror=\"{js}\">"
        div = Div(text=html)
        st.bokeh_chart(div)

def logged_in_title(strava_auth, header=None):
    if header is None:
        base = st
    else:
        col, _, _, _ = header
        base = col

    first_name = strava_auth["athlete"]["firstname"]
    last_name = strava_auth["athlete"]["lastname"]
    col.markdown(f"*Welcome, {first_name} {last_name}!*")


@st.cache(show_spinner=False, suppress_st_warning=True)
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
        st.experimental_set_query_params()
        st.stop()
        return

    strava_auth = response.json()

    return strava_auth

def authenticate(header=None, stop_if_unauthenticated=True):
    query_params = st.experimental_get_query_params()
    authorization_code = query_params.get("code", [None])[0]

    if authorization_code is None:
        authorization_code = query_params.get("session", [None])[0]

    if authorization_code is None:
        login_header(header=header)
        if stop_if_unauthenticated:
            st.stop()
        return
    else:
        logout_header(header=header)
        strava_auth = exchange_authorization_code(authorization_code)
        logged_in_title(strava_auth, header)
        st.experimental_set_query_params(session=authorization_code)

        return strava_auth
