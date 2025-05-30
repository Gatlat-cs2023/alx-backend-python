#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""

import unittest
from unittest import TestCase
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
import requests
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
from parameterized import parameterized_class

class TestGithubOrgClient(TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("case_google", "google", {"login": "google", "id": 1}),
        ("case_abc", "abc", {"login": "abc", "id": 2})
    ])
    @patch("client.get_json")
    def test_org(self, _, org_name, expected_response, mock_get_json):
        """Test that GithubOrgClient.org returns the expected org data."""
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), expected_response)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected repo names"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = (
                "https://api.github.com/orgs/testorg/repos"
            )
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/testorg/repos"
            )
            mock_url.assert_called_once()

    @parameterized.expand([
        (
            {"license": {"key": "my_license"}},  # repo
            "my_license",                        # license_key
            True                                  # expected
        ),
        (
            {"license": {"key": "other_license"}},
            "my_license",
            False
        )
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license correctly detects license matches."""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.has_license(repo, license_key), expected)

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get before tests run, use side_effect to provide different responses."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def get_side_effect(url, *args, **kwargs):
            """Return different payloads depending on the URL."""
            if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                # org endpoint returns org_payload
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.org_payload
                mock_response.status_code = 200
                return mock_response
            elif url == cls.org_payload['repos_url']:
                # repos endpoint returns repos_payload
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.repos_payload
                mock_response.status_code = 200
                return mock_response
            else:
                raise ValueError(f"Unmocked URL called: {url}")

        cls.mock_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo names."""
        client = GithubOrgClient(self.org_payload['login'])
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns repos with apache2 license correctly filtered."""
        client = GithubOrgClient(self.org_payload['login'])
        apache2_repos = client.public_repos(license_key="apache-2.0")
        self.assertEqual(apache2_repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
