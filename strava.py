import streamlit as st

def header():
    col1, col2, col3 = st.columns(3)

    with col3:
        strava_button = st.empty()

    return col1, col2, col3, strava_button


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
