from strava import authenticate
import streamlit as st
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd

st.set_page_config(
    page_title="Streamlit Activity Viewer for Strava",
    page_icon=":circus_tent:",
)

strava_header = authenticate.header()

strava_auth = authenticate.authentication(header=strava_header)


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

    


