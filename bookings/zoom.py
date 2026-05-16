import requests
import base64

ACCOUNT_ID = "MHTOsWebSFeeMaJ5Wzj8lQ"
CLIENT_ID = "MHTOsWebSFeeMaJ5Wzj8lQ"
CLIENT_SECRET = "K1Eckct40xJB5OW9nCYC4ZFV86KsRYl2"


def get_zoom_token():
    url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={ACCOUNT_ID}"

    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}"
    }

    response = requests.post(url, headers=headers)
    return response.json()["access_token"]


def create_zoom_meeting(topic, start_time):
    token = get_zoom_token()

    url = "https://api.zoom.us/v2/users/me/meetings"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "topic": topic,
        "type": 2,
        "start_time": start_time,
        "duration": 30,
        "timezone": "Asia/Kolkata"
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["join_url"]
