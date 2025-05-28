#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import unittest
from unittest import TestCase
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(TestCase):

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2})
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_response, mock_get_json):
        mock_get_json.return_value = mock_response

        client = GithubOrgClient(org_name)
        result = client.org()  # <-- Correct: call the method to get the data

        self.assertEqual(result, mock_response)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url returns correct URL from mocked .org"""
        test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        with patch.object(GithubOrgClient, "org", return_value=test_payload):
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, test_payload["repos_url"])

if __name__ == "__main__":
    unittest.main()
