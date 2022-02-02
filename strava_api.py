import requests
import urllib3
import my_secrets

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
get_all_activities_url = "https://www.strava.com/api/v3/athlete/activities"
get_activity_url = "https://www.strava.com/api/v3/activities"
webhook_subscription_url = "https://www.strava.com/api/v3/push_subscriptions"

auth_payload = {
    'client_id': my_secrets.client_id,
    'client_secret': my_secrets.client_secret,
    'refresh_token': my_secrets.refresh_token,
    'grant_type': "refresh_token",
    'f': 'json'
}

sub_payload = {
    'client_id': my_secrets.client_id,
    'client_secret': my_secrets.client_secret,
    'callback_url': f'http://{my_secrets.ngrok_url}/api/receive_webhook',
    'verify_token': "STRAVA"
}


class StravaApi():
    def sync(self):
        access_token = self.refresh_auth_token()

        header = {'Authorization': 'Bearer ' + access_token}
        param = {'per_page': 5, 'page': 1}
        print("Requesting Activities...\n")
        return requests.get(get_all_activities_url, headers=header, params=param).json()

    def refresh_auth_token(self):
        # do refresh
        print("Requesting Token...\n")
        res = requests.post(auth_url, data=auth_payload, verify=False)
        access_token = res.json()['access_token']
        print("Access Token = {}\n".format(access_token))
        return access_token

    def get_activity(self, activity_id):
        access_token = self.refresh_auth_token()
        res = requests.get(
            f'{get_activity_url}/{activity_id}',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        print(f'got activity, status code: {res.status_code}')
        if res.status_code == 200:
            print(
                f'Got activity info', res.json())
            return res.json()
        return None

    def register_webhook():
        res = requests.post(webhook_subscription_url,
                            data=sub_payload, verify=False)
        print(f'push_subscriptions response {res}')

    def view_webhook_subscriptions():
        param = {'client_id': my_secrets.client_id,
                 'client_secret': my_secrets.client_secret}
        res = requests.get(webhook_subscription_url, params=param)
        if res.status_code == 200:
            print(
                f'Got webhook subscriptions', res.json())
            return res.json()
        return None

    def delete_webhook_subscription(id):
        payload = {
            'id': id,
            'client_id': my_secrets.client_id,
            'client_secret': my_secrets.client_secret
        }
        res = requests.delete(
            f'{webhook_subscription_url}/{id}', data=payload, verify=False)
        print(f'delete_webhook_subscription response {res}')
