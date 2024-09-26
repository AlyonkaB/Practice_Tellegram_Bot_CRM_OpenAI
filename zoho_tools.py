import os
import pprint

import requests
from dotenv import load_dotenv


load_dotenv()


ZOHO_API_TOKEN_URL = os.getenv("ZOHO_API_TOKEN_URL")
ZOHO_API_CRM_URL = os.getenv("ZOHO_API_CRM_URL")
ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")


def get_refresh_token():
    body = {
        "grant_type": "authorization_code",
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "code": "1000.d504933f513c6c47956f45c4d1614ee8.ebe7fe609a29f454164358816cb212f1",
    }
    url = f"{ZOHO_API_TOKEN_URL}?grant_type={body['grant_type']}&client_id={body['client_id']}&client_secret={body['client_secret']}&code={body['code']}"
    response = requests.post(url)
    return response.json()


def get_access_token():
    refresh_token = ZOHO_REFRESH_TOKEN
    client_id = ZOHO_CLIENT_ID
    client_secret = ZOHO_CLIENT_SECRET
    data = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
    }
    # Send the request to the Zoho token endpoint
    token_response = requests.post(ZOHO_API_TOKEN_URL, data=data)
    return token_response.json().get("access_token")


def make_zoho_api_get_request(endpoint):
    zoho_token = get_access_token()
    # print(zoho_token)
    headers = {"Authorization": f"Zoho-oauthtoken {zoho_token}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()

# pprint.pprint(make_zoho_api_get_request(ZOHO_API_CRM_URL))


def create_leads(user_data: dict):
    zoho_token = get_access_token()
    headers = {"Authorization": f"Zoho-oauthtoken {zoho_token}"}
    data = {
        "data": [
            {
                "First_Name": user_data.get("name"),
                "Last_Name": "Last name",
                "Company": "Test company",
                "Email": user_data.get("email"),
                "City": user_data.get("city"),
                "Description": user_data.get("awaiting_feedback"),
            }
        ]
    }
    response = requests.post(ZOHO_API_CRM_URL, headers=headers, json=data)
    return response.json()


def update_lead(lead_id: str, user_data: dict):
    zoho_token = get_access_token()
    headers = {"Authorization": f"Zoho-oauthtoken {zoho_token}"}
    data = {
        "data": [
            {
                "First_Name": user_data.get("name"),
                "Last_Name": user_data.get("last_name"),
                "Company": user_data.get("company"),
                "Email": user_data.get("email"),
                "City": user_data.get("city"),
                "Description": user_data.get("awaiting_feedback"),
            }
        ]
    }
    endpoint = f"{ZOHO_API_CRM_URL}/{lead_id}"
    response = requests.put(endpoint, headers=headers, json=data)
    return response.json()


def delete_lead(lead_id: str):
    zoho_token = get_access_token()
    headers = {"Authorization": f"Zoho-oauthtoken {zoho_token}"}
    endpoint = f"{ZOHO_API_CRM_URL}?ids={lead_id}"
    response = requests.delete(endpoint, headers=headers)
    return response.json()
