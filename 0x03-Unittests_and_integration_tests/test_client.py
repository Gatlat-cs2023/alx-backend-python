#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from unittest import TestCase
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient

# Inline fixtures here as ALX expects everything in one file
org_payload = {
    "login": "google",
    "id": 1,
    "repos_url": "https://api.github.com/orgs/google/repos"
}

repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}}
]

expected_repos = ["repo1", "repo2", "repo3"]

apache2_repos = ["repo1", "repo3"]

"""
Unit tests for GithubOrgClient
"""

class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        # Arrange: Mock return value
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Act: Create client and call .org
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: Check if return matches mock
        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


#!/usr/bin/env python3
"""
Integration test for GithubOrgClient.public_repos
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class

from client import GithubOrgClient

# Define inline fixtures
org_payload = {
    "login": "google",
    "id": 1,
    "repos_url": "https://api.github.com/orgs/google/repos"
}
repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}}
]
expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo1", "repo3"]

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and set fixture responses"""
        cls.get_patcher = patch('requests.get')

        mock_get = cls.get_patcher.start()

        # Side effects for each call to requests.get().json()
        mock_response_org = Mock()
        mock_response_org.json.return_value = cls.org_payload

        mock_response_repos = Mock()
        mock_response_repos.json.return_value = cls.repos_payload

        # Side effect: order of URLs expected
        mock_get.side_effect = [mock_response_org, mock_response_repos]

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after all tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected list of repos"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos by license"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)

if __name__ == "__main__":
    unittest.main()


