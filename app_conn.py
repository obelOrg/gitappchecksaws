import time
import requests
import jwt
import os
import urllib.parse
import json
import http
import http.client
from github import Github
from app_custom.app_custom import GithubIntegration
from flask import Flask, request
app = Flask(__name__)

base_app_url="https://api.github.com/app/installations"
GITHUB_APP_ID = "184311"
def github_request(method, url,github_token, headers=None, data=None, params=None):
    """Execute a request to the GitHUB API, handling redirect"""
    if not headers:
        headers = {}
    headers.update({
        "User-Agent": "application/vnd.github.v3+json",
        "Authorization": "Bearer " + github_token,
    })

    url_parsed = urllib.parse.urlparse(url)
    url_path = url_parsed.path
    if params:
        url_path += "?" + urllib.parse.urlencode(params)

    data = data and json.dumps(data)

    conn = http.client.HTTPSConnection(url_parsed.hostname)
    conn.request(method, url_path, body=data, headers=headers)
    response = conn.getresponse()

    if response.status >= 400:
        headers.pop('Authorization', None)
        raise Exception(
            f"Error: {response.status} - {json.loads(response.read())} - {method} - {url} - {data} - {headers}"
        )

    return (response, json.loads(response.read().decode()))

def read_pemfile(path_pem):
    with open(os.path.normpath(os.path.expanduser(path_pem)),'r') as cert_file:
        private_key = cert_file.read()
    return private_key

def upload_to_github(github_token,owner,repo_name,pr_number):
    # Get last commit SHA of a branch
    #owner = 'mauricioobgo'
    #repo_name = 'runners-test'

    integration = GithubIntegration(integration_id=GITHUB_APP_ID, 
                                private_key=github_token, 
                                base_url="https://github.com/api/v3")
    resp, jeez = github_request("GET", f"{base_app_url}",integration.create_jwt())
    #getting access token
    id_installation=jeez[1]['id']
    resp, jeez = github_request("POST",
            f"{base_app_url}/{id_installation}/access_tokens",
            integration.create_jwt(),
        )
  

    git_connection=Github(jeez['token'])
    repo = git_connection.get_repo(f"{owner}/{repo_name}")
    #issue = repo.get_issue(number=payload['pull_request']['number'])    
    issue = repo.get_issue(number=pr_number)

    # Call meme-api to get a random meme
    response = requests.get(url='https://meme-api.herokuapp.com/gimme')
    if response.status_code != 200:
        return 'ok'
    # Get the best resolution meme
    meme_url = response.json()['preview'][-1]
    # Create a comment with the random meme
    issue.create_comment(f"![Alt Text]({meme_url})")
    return "ok"    

def look_for_pr_numberb(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = look_for_pr_numberb(v, key)
            if item is not None:
                return item

@app.route("/", methods=['POST'])
def bot():
    # Get the event payload
    payload = request.json
    pull_r=look_for_pr_numberb(payload,'pull_requests')
    if pull_r is not None:
        if look_for_pr_numberb(pull_r,'number') is not None:
            owner = payload['repository']['owner']['login']
            repo_name = payload['repository']['name']
            pr_number=pull_r[0]["number"]
            git_identification=read_pemfile('.//.certs//github//gitapppr2.pem')
            upload_to_github(git_identification,owner,repo_name,pr_number)

 

    return "ok"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
