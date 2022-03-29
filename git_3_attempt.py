import github3



GITHUB_PRIVATE_KEY = open('.//.certs//github//gitapppr.pem', 'r').read()
GITHUB_APP_IDENTIFIER = "184311"

gh = github3.github.GitHub()

# Login as app
gh.login_as_app(GITHUB_PRIVATE_KEY.encode(), GITHUB_APP_IDENTIFIER)

# Login to the installation, assuming only a single one
installations = [installation.id for installation in gh.app_installations()]
gh.login_as_app_installation(GITHUB_PRIVATE_KEY.encode(), GITHUB_APP_IDENTIFIER, installations[0])

# Access information
# e.g. the rate limit
print(gh.rate_limit())
# or access token to checkout the repository
print(gh.session.auth.token)