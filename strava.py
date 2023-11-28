

def header():
    col1, col2, col3 = st.beta_columns(3)

    with col3:
        strava_button = st.empty()

    return col1, col2, col3, strava_button
