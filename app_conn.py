import time
import requests
import jwt
import os
from github import Github, GithubIntegration

with open(os.path.normpath(os.path.expanduser('.//.certs//github//gitapppr.pem')),'r') as cert_file:
    private_key = cert_file.read()

GITHUB_APP_ID = "184311"
integration = GithubIntegration(
    GITHUB_APP_ID, private_key, base_url="https://github.com/api/v3")

install = integration.get_installation('mauricioobgo' ,'obelOrg/gitappchecksaws')
access = integration.get_access_token(install.id)
# And here it is :)
print(access.token)

gh = Github(login_or_token=access.token,
            base_url="https://github.com/api/v3")