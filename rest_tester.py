import requests
import json
import pandas as pd
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
import base64
import xml.etree.ElementTree as ET

xml_fact = ''
with open("data/facturaFirmada1.xml", "rb") as file:
    xml_fact = file.read()

b = bytearray()
# b.extend(map(ord, xml_fact))
# print(xml_fact)

xml_base64 = base64.b64encode(xml_fact).decode("utf-8")
# print(xml_base64)


# xml_fact_ET = ET.tostring(ET.parse("data/facturaFirmada1.xml").getroot())
# xml_fact_ET = ET.tostring(ET.fromstring(xml_fact))
# xml_base64_ET = base64.b64encode(xml_fact_ET).decode("utf-8")
# print(xml_base64_ET)
#
# xml_decode = base64.b64decode(xml_base64)
# print(xml_decode)
# xml_decode_ET = base64.b64decode(xml_base64_ET)
# print(xml_decode_ET)

df = pd.DataFrame()
print(df)

sandbox_api_comprobantes = "https://api.comprobanteselectronicos.go.cr/recepcion-sandbox/v1/comprobantes"
sandbox_api_recepcion = "https://api.comprobanteselectronicos.go.cr/recepcion-sandbox/v1/recepcion"

prod_api_comprobantes = "https://api.comprobanteselectronicos.go.cr/recepcion/v1/comprobantes"
prod_api_recepcion = "https://api.comprobanteselectronicos.go.cr/recepcion/v1/recepcion"

access_token_stag_url = "https://idp.comprobanteselectronicos.go.cr/auth/realms/rut-stag/protocol/openid-connect/token"
access_token_prod_url = "https://idp.comprobanteselectronicos.go.cr/auth/realms/rut/protocol/openid-connect/token"


login_stag = {'client_id': 'api-stag',  # Test: 'api-stag' Production: 'api-prod'
        'username': 'cpf-04-0209-0351@stag.comprobanteselectronicos.go.cr',
        'password': 'B4*=(Oe^=WzK*h$*[9>y',
        'grant_type': 'password',  # always 'password'
        'client_secret': '',  # always empty
        'scope': ''  # always empty
}

login_prod = {
    'client_id': 'api-prod',  # Test: 'api-stag' Production: 'api-prod'
    'username': 'cpf-04-0209-0351@prod.comprobanteselectronicos.go.cr',
    'password': '/Y.0M{p[{i@H8?Z0/?!5',
    'grant_type': 'password',  # always 'password'
    'client_secret': '',  # always empty
    'scope': ''  # always empty

}

stag_oauth = OAuth2Session(client=LegacyApplicationClient(client_id=login_stag['client_id']))
stag_token = stag_oauth.fetch_token(token_url=access_token_stag_url,
                          username=login_stag['username'], password=login_stag['password'], client_id=login_stag['client_id'],
                          client_secret='')

prod_oauth = OAuth2Session(client=LegacyApplicationClient(client_id=login_prod['client_id']))
prod_token = prod_oauth.fetch_token(token_url=access_token_prod_url,
                          username=login_prod['username'], password=login_prod['password'], client_id=login_prod['client_id'],
                          client_secret='')
print("prod_token: ", json.dumps(prod_token, indent=4, sort_keys=True))

params_comprobantes = {
    "limit": 1,
    "offset": 0,
    "emisor": "",
    "callbackuri": "",
    "receptor": "",
    "Authorization: Bearer ": stag_token['access_token'],
    # "Cache-Control": "no-cache",
    # "Postman-Token": "bf8dc171-5bb7-fa54-7416-56c5cda9bf5c",
    "Content-Type": "application/x-www-form-urlencoded",
}
t = {'true': 'true'}

headers = {
    'Authorization': 'bearer %s' % stag_token['access_token'],
    'Content-Type': 'application/json'
}
prod_headers = {
    'Authorization': 'bearer %s' % prod_token['access_token'],
    'Content-Type': 'application/json'
}

recepcion = {
    "clave": "50601011600310112345600100010100000000011999999999",
    "fecha": "2016-01-01T00:00:00-0600",
    "emisor": {
        "tipoIdentificacion": "02",
        "numeroIdentificacion": "3101123456"
    },
    "receptor": {
        "tipoIdentificacion": "02",
        "numeroIdentificacion": "3101123456"
    },
    "comprobanteXml": xml_base64
}


# print(json.dumps(recepcion, indent=4, sort_keys=True))



def getComprobantes():
    get_comp = requests.get(prod_api_comprobantes,  # +"/506010116003101123456001000101000000011999999999",
                            headers=prod_headers, params=t)
    if get_comp.ok:
        print(json.dumps(get_comp.json(), indent=4, sort_keys=True))
    else:
        print(get_comp.status_code, json.loads(get_comp._content or '{}'))


def postRecepcion():
    post_recepcion = requests.post(sandbox_api_recepcion, headers=headers, )
    if post_recepcion.ok:
        print(post_recepcion.status_code)
        print(json.dumps(post_recepcion.json(), indent=4, sort_keys=True))
    else:

        print(post_recepcion.status_code, json.loads(post_recepcion._content or '{}'))


getComprobantes()
# postRecepcion()
