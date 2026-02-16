import requests
import base64

ACCOUNT_ID = "uU4bnC8_QYaKxWlNi9pbrQ"
CLIENT_ID = "lm5xl_dQQ3SKstOguzYjQ"
CLIENT_SECRET = "nlpB6KLgx2BRjRUHQLrfpI861DUoKd4D"


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
