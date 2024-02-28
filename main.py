from strava import authenticate, analysis
import streamlit as st
# import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd
from datetime import timedelta

st.set_page_config(
    page_title="Streamlit Activity Viewer for Strava",
    page_icon=":circus_tent:",
)

strava_header = authenticate.header()

strava_auth = authenticate.authentication(header=strava_header)
# st.write(strava_auth)


if strava_auth is None:
    # st.markdown("Use the **Connect with Strava** button at the top of the screen to login!")
    st.warning('Please use the Connect with Strava button to login!')
    st.stop()

refresh_token = authenticate.refresh_from_authentication(strava_auth)

id = analysis.athlete_id(refresh_token)
total_runs = analysis.number_of_runs(refresh_token, id) 
num_pages = int(total_runs/200) + 1
activities = []
for i in range(num_pages):
    page = i + 1
    page_activities = analysis.get_activities(refresh_token, page)
    activities.extend(page_activities)
# st.json(activities) 

fastest_times = []
for i in activities[:30]:
    activity_id = i["id"]
    name = i["name"]
    kms = i["distance"] / 1000

    stream = analysis.activity_stream(refresh_token, activity_id)

    fastest_km_time = analysis.activity_fastest_km(stream[0], stream[1])
    # fastest_km_time = analysis.convertSecs(fastest_km_time)

    fastest_five_km_time = analysis.activity_fastest_five_km(stream[0], stream[1])
    fastest_ten_km_time = analysis.activity_fastest_ten_km(stream[0], stream[1])
    fastest_half_time = analysis.activity_fastest_half(stream[0], stream[1])
    fastest_mara_time = analysis.activity_fastest_mara(stream[0], stream[1])

    fastest_times.append([str(activity_id), name, kms, fastest_km_time, fastest_five_km_time, fastest_ten_km_time, fastest_half_time, fastest_mara_time])

df = pd.DataFrame(fastest_times, columns=['activity_id', 'name', 'kms', '1km', '5km', '10km', 'Half', 'Marathon'])
df[['1km', '5km', '10km', 'Half', 'Marathon']] = df[['1km', '5km', '10km', 'Half', 'Marathon']].applymap(analysis.convertSecs)
st.dataframe(df)



old_table = authenticate.convert_json_to_df(activities)
st.dataframe(old_table)





# st.write(strava_auth)



# if strava_auth is None:
#     st.markdown("Use the **Connect with Strava** button at the top of the screen to login!")
#     st.warning('Please login!')
#     # st.stop
#     # st.exception("Please login!")
# else:
#     # st.success("Thanks for logging in")
#     st.header("Strava Activities")

#     activities = []
#     json_activities = strava.get_activities(strava_auth, page=1)
#     json_activities_2 = strava.get_activities(strava_auth, page=2)
#     activities.extend(json_activities)
#     activities.extend(json_activities_2)
#     st.json(activities)

#     slider = strava.activities_slider(activities)
#     activity_table = strava.convert_json_to_df(activities) # ADDED LINE
#     filtered_table = strava.filter_activities_from_slider(activity_table, slider)

#     st.dataframe(
#         filtered_table, 
#         column_config={"Link to Activity": st.column_config.LinkColumn()
#                       },
#         hide_index=True
#     )

#     st.header("Headline Numbers")
#     distance = strava.adding_headline_numbers(filtered_table)
#     st.write('You ran', distance, 'kms during the specified date range')

    ##############################
    ########### Adding Histogram - functionalise this in strava.py later
    ##############################
    
    # from matplotlib.ticker import FormatStrFormatter # put here so I remember to move it into strava.py
    # st.header("Run Distribution by Distance (kms)")
    
    # fig, ax = plt.subplots()
    # ax.set_facecolor('#eafff5')

    # data = filtered_table['Distance (km)']
    # w=5
    # counts, bins, patches = ax.hist(data, bins=np.arange(0, max(data) + w, w), rwidth=1, facecolor='yellow', edgecolor='black')

    # ax.set_xticks(bins)
    # ax.xaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
    # plt.xlabel('Kms per Run')
    # plt.ylabel('Count')
    # ax.xaxis.labelpad = 20

    # # Change the colors of bars at the edges...
    # twentyfifth, seventyfifth = np.percentile(data, [25, 75])
    # for patch, rightside, leftside in zip(patches, bins[1:], bins[:-1]): # the first rightside bin is at bins[1] and the last leftside patch is at bins[-1]
    #     if rightside < twentyfifth:
    #         patch.set_facecolor('green')
    #     elif leftside > seventyfifth:
    #         patch.set_facecolor('red')

    # # 2 lines to get y-coordinate for placement of raw count label
    # max_height = max([x.get_height() for x in patches]) # height of tallest histogram bin
    # label_placement = (max_height * 4/107) 
    
    # bin_centers = 0.5 * np.diff(bins) + bins[:-1]
    # for count, x, patch in zip(counts, bin_centers, patches):
    #     # Label the raw counts
    #     ax.annotate(str(count), xy=(x, 0), xycoords=('data', 'axes fraction'),
    #         xytext=(0,patch.get_height() + label_placement), textcoords=('offset points', 'data'), va='top', ha='center')
        
    #     # Label the percentages
    #     percent = '%0.0f%%' % (100 * float(count) / counts.sum())
    #     ax.annotate(percent, xy=(x, 0), xycoords=('data', 'axes fraction'),
    #         xytext=(0, -16), textcoords='offset points', va='top', ha='center')
    
    # st.pyplot(fig)

    


