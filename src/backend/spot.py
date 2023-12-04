import requests
import uuid
import urllib
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# needs to be within endpoints with callback
class Spot:
    def __init__(self, cid, secret, redirect) -> None:
        self.CLIENT_ID = cid
        str = cid + ":" + secret
        self.BASE64_AUTH_STR = base64.b64encode(str.encode()).decode('utf-8')
        self.REDIRECT_URI = redirect
        self.callback = False
        options = Options()
        options.add_argument('--headless')
        self.BROWSER = webdriver.Chrome(options=options)
        self.authenticated = False

    ACCESS_TOKEN = ''

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

        self.BROWSER.quit();
        options = Options()
        options.add_experimental_option("detach", True)
        self.BROWSER = webdriver.Chrome(options=options)
        self.BROWSER.get(auth_url) 

    def tab(self, tab):
        self.BROWSER.switch_to.window(tab)

    def close_tab(self, tab=''):
        if tab == 'default': 
            self.BROWSER.switch_to.window(self.BROWSER.window_handles[0])
        elif tab != '':
            self.tab(tab)

        self.BROWSER.close()
    
    def close_browser(self):
        self.BROWSER.quit()


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
                    
    # returns response json for parsing
    # expects body to be json
    def request(self, url, param):
        header = {
            'Authorization': f'Bearer {self.ACCESS_TOKEN}'
        }

        response: requests.Response = requests.get(url, headers=header, params=param)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Failed Request. Response: {response.text}')