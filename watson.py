import requests as r
from requests.auth import HTTPBasicAuth

UN = "aee0f544-c56c-49f3-a529-43ef19047960"
PW = "elnmzTVIm1cI"

print(r.get("https://gateway.watsonplatform.net/tone-analyzer-beta/api/v3/tone?version=2016-02-11&text={}".format("Apple expected to win!"),
                                                                                                                  auth=HTTPBasicAuth(UN, PW)).text)