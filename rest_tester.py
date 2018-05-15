import requests
import json

sandbox_api = "https://api.comprobanteselectronicos.go.cr/recepcion-sandbox/v1/"
access_token_url = "https://idp.comprobanteselectronicos.go.cr/auth/realms/rut-stag/protocol/openid-connect/token"

data = {'client_id':'api-stag',#Test: 'api-stag' Production: 'api-prod'
        'username': "cpf-04-0209-0351@stag.comprobanteselectronicos.go.cr",
        'password': "asdasdasdsadsadsadasd",
        'grant_type': "password", #always 'password'
        'client_secret': '',#always empty
        'scope':''#always empty
}

resp = requests.post(access_token_url, data=data)
resp_token_sandbox = resp.json()
print(json.dumps(resp.json(), indent=4, sort_keys=True))
# print(type(resp), "  -  ", type(resp.json()))

params_comprobantes = {'limit': 1,
                     'Authorization: Bearer': resp_token_sandbox['access_token']}
resp_comprobantes = requests.get(sandbox_api, params=params_comprobantes)
print(json.dumps(resp_comprobantes.json(), indent=4, sort_keys=True))


from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

oauth = OAuth2Session(client=LegacyApplicationClient(client_id=data['client_id']))
token = oauth.fetch_token(token_url=access_token_url,
        username=data['username'], password=data['password'], client_id=data['client_id'],
        client_secret='')

