import requests

def get_json(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

class GithubOrgClient:
    def __init__(self, org_name):
        self.org_name = org_name

    def org(self):
        """Return the organization data as dict."""
        return get_json(f"https://api.github.com/orgs/{self.org_name}")

    @property
    def _public_repos_url(self):
        """Return the repos_url from the org data."""
        return self.org().get("repos_url")

    def _public_repos(self):
        """Return the list of public repos from the repos URL."""
        return get_json(self._public_repos_url)

    def public_repos(self, license=None):
        repos = self._public_repos()
        if license is None:
            return [repo["name"] for repo in repos]
        return [
            repo["name"] for repo in repos
            if repo.get("license", {}).get("key") == license
        ]

    def has_license(self, repo, license_key):
        """Check if the repo has the specified license."""
        return repo.get("license", {}).get("key") == license_key
