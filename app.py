import os
import requests
import jwt
from flask import Flask, request
from github import Github, GithubIntegration


app = Flask(__name__)
# MAKE SURE TO CHANGE TO YOUR APP NUMBER!!!!!
app_id = '184311'
# Read the bot certificate
with open(
        os.path.normpath(os.path.expanduser('.//.certs//github//gitapppr.pem')),
        'r',encoding="utf-8") as cert_file:
    app_key = cert_file.read()

# Create an GitHub integration instance
git_integration = GithubIntegration(
    app_id,
    app_key,
)

access_tokens_url = 'https://github.com/api/v3/app/installations/{installation_id}/access_tokens'.format(installation_id=app_id)
headers={'Authorization': 'Bearer '+ app_key}

@app.route("/", methods=['POST'])
def bot():
    # Get the event payload
    payload = request.json

    # Check if the event is a GitHub PR creation event
    if not all(k in payload.keys() for k in ['action', 'pull_request']) and \
            payload['action'] == 'opened':
        return "ok"

    owner = payload['repository']['owner']['login']
    repo_name = payload['repository']['name']
    # Get a git connection as our bot
    # Here is where we are getting the permission to talk as our bot and not
    # as a Python webservice

    git_connection = Github(access_tokens_url,app_key)
 
    repo = git_connection.get_repo(f"{owner}/{repo_name}")
    issue = repo.get_issue(number=3)

    # Call meme-api to get a random meme
    response = requests.get(url='https://meme-api.herokuapp.com/gimme')

    if response.status_code != 200:
        return 'ok'

    # Get the best resolution meme
    meme_url = response.json()['preview'][-1]
    print(meme_url)
    # Create a comment with the random meme
    issue.create_comment(f"![Alt Text]({meme_url})")
    print("ok awesome")
    return "ok"


if __name__ == "__main__":
    app.run(debug=True, port=5000)