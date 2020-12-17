import requests

OKTA_BASE_PATH = "https://dev-2337597.okta.com"
USER_INFO_ENDPOINT = "/oauth2/default/v1/userinfo"


def get_user_profile(auth_header):
    url = OKTA_BASE_PATH + USER_INFO_ENDPOINT

    response = requests.get(url=url, headers={
        "Accept": "application/json",
        "Authorization": auth_header
    })

    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        return None
