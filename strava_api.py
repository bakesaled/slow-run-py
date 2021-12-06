import requests
import urllib3

import pandas as pd
from pandas import json_normalize

# Seaborn is a data visualization library.
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

import secrets

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': secrets.cliend_id,
    'client_secret': secrets.client_secret,
    'refresh_token': secrets.refresh_token,
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 100, 'page': 1}
print("Requesting Activities...\n")
my_dataset = requests.get(activites_url, headers=header, params=param).json()

# print(my_dataset[0]["name"])
# print(my_dataset[0]["map"]["summary_polyline"])
print("Activities retrieved...\n")
activities = json_normalize(my_dataset)
# activities.columns #See a list of all columns in the table
# activities.shape #See the dimensions of the table.

cols = ['name', 'upload_id', 'type', 'distance', 'moving_time',
        'average_speed', 'max_speed', 'total_elevation_gain',
        'start_date_local'
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
