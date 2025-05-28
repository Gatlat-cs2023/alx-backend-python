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
        result = client.org()  # <-- CALL THE METHOD HERE

        self.assertEqual(result, mock_response)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


if __name__ == "__main__":
    unittest.main()
