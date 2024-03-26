from strava import authenticate, analysis
import streamlit as st


st.set_page_config(
    page_title="Strava Personal Best Viewer",
    page_icon=":runner:",
)

strava_header = authenticate.header()
strava_auth = authenticate.authentication(header=strava_header)
# st.write(strava_auth)

st.markdown(
    """
    # :runner: Strava Personal Best Viewer

    This is a proof of concept Streamlit application which shows users their 1km, 5km, 10km, half and marathon personal bests over a given time period.
    
    The app implements the [Strava API](https://developers.strava.com/) OAuth2 authentication flow to allow viewers to see their indivudual personal bests."""
)

if strava_auth is None:
    st.warning('Please use the Connect with Strava button to login!')
    st.stop()


refresh_token = authenticate.refresh_from_authentication(strava_auth)

with st.spinner(f"Generating date slider to filter Strava activities"):
    activities = analysis.full_activity_list(refresh_token)

    if len(activities) == 0:
        st.warning("Your Strava Account doesn't have any public running activities")
        st.stop()

    slider = analysis.activities_slider(activities)

with st.spinner(f"Generating fastest splits for Strava activities"):
    df = analysis.create_dataframe(activities, refresh_token)
    filtered_table = analysis.filter_activities_from_slider(df, slider)

    st.dataframe(
        filtered_table, 
        column_config={"Activity ID": st.column_config.LinkColumn(
            display_text="View on Strava" # '\/activities\/(\d+)'
        )
                        },
        hide_index=True
    )


## Optional Histogram, showing run distribution by distance for the time period the user selects with the slider   
# st.header("Run Distribution by Distance (kms)")
# analysis.run_length_histogram(filtered_table)


# st.header("Headline Numbers")
# distance = strava.adding_headline_numbers(filtered_table)
# st.write('You ran', distance, 'kms during the specified date range')




    


