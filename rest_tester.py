import requests
import json

sandbox_api = "https://api.comprobanteselectronicos.go.cr/recepcion-sandbox/v1/comprobantes"
sandbox_api_recepcion = "https://api.comprobanteselectronicos.go.cr/recepcion-sandbox/v1/recepcion"

access_token_url = "https://idp.comprobanteselectronicos.go.cr/auth/realms/rut-stag/protocol/openid-connect/token"

data = {'client_id':'api-stag',#Test: 'api-stag' Production: 'api-prod'
        'username': 'cpf-04-0209-0351@stag.comprobanteselectronicos.go.cr',
        'password': 'B4*=(Oe^=WzK*h$*[9>y   ',
        'grant_type': 'password', #always 'password'
        'client_secret': '',#always empty
        'scope':''#always empty
}

resp = requests.post(access_token_url, data=data)
resp_token_sandbox = resp.json()
print(json.dumps(resp.json(), indent=4, sort_keys=True))
# print(type(resp), "  -  ", type(resp.json()))

params_comprobantes = { 'limit': 1,
                        'offset': 0,
                        'emisor': '',
                        'receptor': '',
                        'callbackuri' : ''

                        #'Authorization: Bearer ': resp_token_sandbox['access_token'],
                        #"Cache-Control": "no-cache",
                        #"Content-Type": "application/x-www-form-urlencoded",
                        #"Postman-Token": "bf8dc171-5bb7-fa54-7416-56c5cda9bf5c"
                       }
headers = {
    'Authorization': resp_token_sandbox['access_token'],
    #'Authorization: bearer '.params_get('token'),
	'Content-Type': 'application/json'
}

recepcion = {
    "clave": "123",
    "comprobanteXml": "comprobanteXml",
    "consecutivoReceptor": "consecutivoReceptor",
    "emisor": {
        "numeroIdentificacion": "emi_numeroIdentificacion",
        "tipoIdentificacion": "emi_tipoIdentificacion"
    },
    "fecha": "",
    "receptor": {
        "numeroIdentificacion": "recp_numeroIdentificacion",
        "tipoIdentificacion": "recp_tipoIdentificacion"
    }
}
#print(json.dumps(recepcion, indent=4, sort_keys=True))

post_comprobantes = requests.post(sandbox_api_recepcion, headers=headers, data=recepcion)
print(json.dumps(post_comprobantes.json(), indent=4, sort_keys=True))









resp_comprobantes = requests.get(sandbox_api, headers=headers, params=params_comprobantes, data=params_comprobantes)
print(json.dumps(resp_comprobantes.json(), indent=4, sort_keys=True))





from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

oauth = OAuth2Session(client=LegacyApplicationClient(client_id=data['client_id']))
token = oauth.fetch_token(token_url=access_token_url,
        username=data['username'], password=data['password'], client_id=data['client_id'],
        client_secret='')
print(json.dumps(token, indent=4, sort_keys=True))

print(type(token))
import time
print (time.time())
print(time.ctime(token['expires_at']))



