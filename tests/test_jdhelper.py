import unittest
from unittest.mock import patch, Mock
from animeloads.jdhelper import *

class TestJDHelper(unittest.TestCase):
    def test_decode_cnl(self):
        crypted = "emyIg+yDDQz6T+CuG8LdHNARCT9u5yEr4dzRjKhxy5yuqvYSsBGlGbS1RsAK+fQmWHfYxi936txEwQ30w6n3qO8oViHiY8HutF1raTKdl/JJ1CR42TsvvxRj0oFopFUR"
        k = "50764e7531304244446463703948524a"
        result = decode_cnl(k, crypted)
        shouldResult = [b"https://ddownload.com/mm7zy52079so?[AMALGAM]Conan_Aufklaerungsfilm[624x480][x264].rar"]
        self.assertEqual(result, shouldResult, "Failed to decode CNL")

    @patch('requests.post')
    def test_add_to_jd_success(self, mock_post):
        host = "testhost.com"
        passwords = "TestPassword"
        source = "TestSource"
        crypted = "emyIg+yDDQz6T+CuG8LdHNARCT9u5yEr4dzRjKhxy5yuqvYSsBGlGbS1RsAK+fQmWHfYxi936txEwQ30w6n3qO8oViHiY8HutF1raTKdl/JJ1CR42TsvvxRj0oFopFUR"
        k = "50764e7531304244446463703948524a"

        expected_response = "success"
        mock_response = Mock()
        mock_response.text.return_value = expected_response
        mock_post.return_value = mock_response

        actual_response = add_to_jd(host, passwords, source, crypted, k)

        self.assertEqual(actual_response, True, "Failed to add to JD")
        mock_post.assert_called_once_with('http://testhost.com:9666/flash/addcrypted2', data={'passwords': 'TestPassword', 'source': 'TestSource', 'jk': '50764e7531304244446463703948524a', 'crypted': 'emyIg+yDDQz6T+CuG8LdHNARCT9u5yEr4dzRjKhxy5yuqvYSsBGlGbS1RsAK+fQmWHfYxi936txEwQ30w6n3qO8oViHiY8HutF1raTKdl/JJ1CR42TsvvxRj0oFopFUR'}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0 Waterfox/78.7.0'}, timeout=30)
        mock_response.text.assert_called_once()


    @patch('requests.post')
    def test_add_to_jd_failed(self, mock_post):
        host = "testhost.com"
        passwords = "TestPassword"
        source = "TestSource"
        crypted = "emyIg+yDDQz6T+CuG8LdHNARCT9u5yEr4dzRjKhxy5yuqvYSsBGlGbS1RsAK+fQmWHfYxi936txEwQ30w6n3qO8oViHiY8HutF1raTKdl/JJ1CR42TsvvxRj0oFopFUR"
        k = "50764e7531304244446463703948524a"

        expected_response = "failed"
        mock_response = Mock()
        mock_response.text.return_value = expected_response
        mock_post.return_value = mock_response

        actual_response = add_to_jd(host, passwords, source, crypted, k)

        self.assertEqual(actual_response, False, "Failed to add to JD")
        mock_post.assert_called_once_with('http://testhost.com:9666/flash/addcrypted2', data={'passwords': 'TestPassword', 'source': 'TestSource', 'jk': '50764e7531304244446463703948524a', 'crypted': 'emyIg+yDDQz6T+CuG8LdHNARCT9u5yEr4dzRjKhxy5yuqvYSsBGlGbS1RsAK+fQmWHfYxi936txEwQ30w6n3qO8oViHiY8HutF1raTKdl/JJ1CR42TsvvxRj0oFopFUR'}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0 Waterfox/78.7.0'}, timeout=30)
        mock_response.text.assert_called_once()