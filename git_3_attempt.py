import time
import jwt
import os
import requests
with open(os.path.normpath(os.path.expanduser('.//.certs//github//gitapppr.pem')),'r') as cert_file:
    private_key = cert_file.read()
def app_headers():

    time_since_epoch_in_seconds = int(time.time())
    
    payload = {
      # issued at time
      'iat': time_since_epoch_in_seconds,
      # JWT expiration time (10 minute maximum)
      'exp': time_since_epoch_in_seconds + (10 * 60),
      # GitHub App's identifier
      'iss': '4397'
    }

    actual_jwt = jwt.encode(payload, private_key, algorithm='RS256')

    headers = {"Authorization": "Bearer {}".format(actual_jwt),
               "Accept": "application/vnd.github.machine-man-preview+json"}
    return headers

resp = requests.get('https://api.github.com/app', headers=app_headers())

print('Code: ', resp.status_code)
print('Content: ', resp.content.decode())