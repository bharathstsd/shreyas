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
        "Authorization": f"Basic {encoded}",
        "Accept": "application/json",
    }

    try:
        response = requests.post(url, headers=headers, timeout=10)
    except requests.RequestException as exc:
        raise RuntimeError(f"Zoom token request failed: {exc}") from exc

    # parse JSON safely and provide helpful error when access_token missing
    try:
        data = response.json()
    except ValueError:
        raise RuntimeError(f"Zoom token response not JSON (status={response.status_code}): {response.text}")

    if response.status_code != 200 or "access_token" not in data:
        # include limited details to help debugging without exposing secrets
        err = data.get("error") or data.get("message") or data
        raise RuntimeError(f"Failed to obtain Zoom access token: {err}")

    return data["access_token"]


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
