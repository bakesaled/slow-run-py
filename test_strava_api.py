import pandas as pd
from pandas import json_normalize

# Seaborn is a data visualization library.
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

from strava_api import StravaApi

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

my_dataset = StravaApi.sync()


# print(my_dataset[0]["name"])
# print(my_dataset[0]["map"]["summary_polyline"])
print(my_dataset)
print("Activities retrieved...\n")
activities = json_normalize(my_dataset)
# activities.columns #See a list of all columns in the table
# activities.shape #See the dimensions of the table.

cols = ['name', 'id', 'upload_id', 'type', 'distance', 'moving_time',
        'average_speed', 'max_speed', 'total_elevation_gain',
        'start_date_local',
        'has_heartrate',
        'average_heartrate',
        'max_heartrate',
        'average_watts',
        'max_watts',
        'kilojoules',
        'elev_high',
        'elev_low',
        ]
activities = activities[cols]
activities['start_date_local'] = pd.to_datetime(activities['start_date_local'])
activities['start_time'] = activities['start_date_local'].dt.time
activities['start_date_local'] = activities['start_date_local'].dt.date
print("Activities formatted...\n")
formatted_activities = activities.head(5)
print(formatted_activities)

runs = activities.loc[activities['type'] == 'Run']
# sns.set(style="ticks", context="talk")
# sns.regplot(x='distance', y='average_speed', data=runs).set_title(
#     "Average Speed vs Distance")
# plt.show()


fig = plt.figure()  # create overall container
ax1 = fig.add_subplot(111)  # add a 1 by 1 plot to the figure
x = np.asarray(runs.start_date_local)  # convert data to numpy array
y = np.asarray(runs.average_speed)
ax1.plot_date(x, y)  # plot data points in scatter plot on ax1
ax1.set_title('Average Speed over Time')
# ax1.set_ylim([0,5])
# add trend line
x2 = mdates.date2num(x)
z = np.polyfit(x2, y, 1)
p = np.poly1d(z)
plt.plot(x, p(x2), 'r--')
# format the figure and display
fig.autofmt_xdate(rotation=45)
fig.tight_layout()
fig.show()

plt.show()
