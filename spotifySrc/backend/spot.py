from flask import redirect
import requests
import uuid
import urllib
import base64
import webbrowser

# needs to be within endpoints with callback
class Spot:
    def __init__(self, cid, secret, redirect) -> None:
        self.CLIENT_ID = cid
        str = cid + ":" + secret
        self.BASE64_AUTH_STR = base64.b64encode(str.encode()).decode('utf-8')
        self.REDIRECT_URI = redirect
        self.callback = False

    ACCESS_TOKEN = ''
    USER_ID = ''

    def authorize(self, scope):
        auth_request_params = {
            'client_id': self.CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': self.REDIRECT_URI,
            'state': str(uuid.uuid4()),
            'scope': scope,
            'show_dialog': 'true'
        }

        self.callback = True

        auth_url = 'https://accounts.spotify.com/authorize/?' + urllib.parse.urlencode(auth_request_params)

        webbrowser.open(auth_url)

    def get_token(self, code):
        endpoint = 'https://accounts.spotify.com/api/token/?'

        body = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.REDIRECT_URI
        } 

        header = {
            'Authorization': 'Basic ' + self.BASE64_AUTH_STR,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response: requests.Response = requests.post(endpoint, data=body, headers=header)
        if response.status_code == 200:
            return response.json()
        
        raise Exception(f'Failed to obtain Access Token. Response: {response.text}')
    
    def get_profile(self):
        profile_url = 'https://api.spotify.com/v1/me'
        header = {
            'Authorization': f'Bearer {self.ACCESS_TOKEN}'
        }

        response: requests.Response = requests.get(profile_url, headers=header)
        if response.status_code == 200:
            response = response.json()
            self.USER_ID = str(response['id'])
            
        else:
            raise Exception(f'Failed to get profile. Response: {response.text}')
            
    # returns response json for parsing
    # expects body to be json
    def request(self, url, body):
        header = {
            'Authorization': f'Bearer {self.ACCESS_TOKEN}'
        }

        response: requests.Response = requests.get(url, headers=header, params=body)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Failed to search. Response: {response.text}')