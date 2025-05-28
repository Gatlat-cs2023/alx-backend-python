#!/usr/bin/env python3
import requests


def get_json(url: str) -> dict:
    """Makes a GET request to the specified URL and returns the JSON response."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


class GithubOrgClient:
    """GithubOrgClient fetches information about GitHub organizations."""

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    def org(self) -> dict:
        """Returns the JSON response from the GitHub organization API."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)
