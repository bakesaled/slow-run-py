import requests
import urllib3
import secrets

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': secrets.client_id,
    'client_secret': secrets.client_secret,
    'refresh_token': secrets.refresh_token,
    'grant_type': "refresh_token",
    'f': 'json'
}


class StravaApi():
    def sync():
        print("Requesting Token...\n")
        res = requests.post(auth_url, data=payload, verify=False)
        access_token = res.json()['access_token']
        print("Access Token = {}\n".format(access_token))

        header = {'Authorization': 'Bearer ' + access_token}
        param = {'per_page': 5, 'page': 1}
        print("Requesting Activities...\n")
        return requests.get(activites_url, headers=header, params=param).json()



