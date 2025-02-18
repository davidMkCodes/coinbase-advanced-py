import unittest
from io import StringIO

from requests.exceptions import HTTPError
from requests_mock import Mocker

from coinbase.__version__ import __version__
from coinbase.rest import RESTClient
from tests.constants import TEST_API_KEY, TEST_API_SECRET


class RestBaseTest(unittest.TestCase):
    def test_no_api_key(self):
        with self.assertRaises(Exception):
            RESTClient(None, None)

        with self.assertRaises(Exception):
            RESTClient("test_key", None)

    def test_get(self):
        client = RESTClient(TEST_API_KEY, TEST_API_SECRET)

        expected_response = {"key_1": "value_1", "key_2": "value_2"}

        with Mocker() as m:
            m.request(
                "GET",
                "https://api.coinbase.com/api/v3/brokerage/accounts",
                json=expected_response,
            )

            params = {"limit": 2}
            kwargs = {"test_kwarg": "test"}
            accounts = client.get("/api/v3/brokerage/accounts", params, **kwargs)

            captured_request = m.request_history[0]
            captured_query = captured_request.query
            captured_headers = captured_request.headers

            self.assertEqual(captured_request.method, "GET")

            self.assertEqual(captured_query, "limit=2&test_kwarg=test")

            self.assertTrue("User-Agent" in captured_headers)
            self.assertEqual(
                captured_headers["User-Agent"], "coinbase-advanced-py/" + __version__
            )
            self.assertTrue("Authorization" in captured_headers)
            self.assertTrue(captured_headers["Authorization"].startswith("Bearer "))

            self.assertEqual(accounts, expected_response)

    def test_post(self):
        client = RESTClient(TEST_API_KEY, TEST_API_SECRET)

        expected_response = {"key_1": "value_1", "key_2": "value_2"}

        with Mocker() as m:
            m.request(
                "POST",
                "https://api.coinbase.com/api/v3/brokerage/portfolios",
                json=expected_response,
            )

            data = {"name": "TestName"}
            kwargs = {"test_kwarg": "test"}

            portfolio = client.post("/api/v3/brokerage/portfolios", data=data, **kwargs)

            captured_request = m.request_history[0]
            captured_json = captured_request.json()
            captured_headers = captured_request.headers

            self.assertEqual(captured_request.method, "POST")

            self.assertEqual(captured_json, {"name": "TestName", "test_kwarg": "test"})

            self.assertTrue("User-Agent" in captured_headers)
            self.assertEqual(
                captured_headers["User-Agent"], "coinbase-advanced-py/" + __version__
            )
            self.assertTrue("Authorization" in captured_headers)
            self.assertTrue(captured_headers["Authorization"].startswith("Bearer "))

            self.assertEqual(portfolio, expected_response)

    def test_put(self):
        client = RESTClient(TEST_API_KEY, TEST_API_SECRET)

        expected_response = {"key_1": "value_1", "key_2": "value_2"}

        with Mocker() as m:
            m.request(
                "PUT",
                "https://api.coinbase.com/api/v3/brokerage/portfolios/1234",
                json=expected_response,
            )

            data = {"name": "TestName"}
            kwargs = {"test_kwarg": "test"}

            portfolio = client.put(
                "/api/v3/brokerage/portfolios/1234", data=data, **kwargs
            )

            captured_request = m.request_history[0]
            captured_json = captured_request.json()
            captured_headers = captured_request.headers

            self.assertEqual(captured_request.method, "PUT")

            self.assertEqual(captured_json, {"name": "TestName", "test_kwarg": "test"})

            self.assertTrue("User-Agent" in captured_headers)
            self.assertEqual(
                captured_headers["User-Agent"], "coinbase-advanced-py/" + __version__
            )
            self.assertTrue("Authorization" in captured_headers)
            self.assertTrue(captured_headers["Authorization"].startswith("Bearer "))

            self.assertEqual(portfolio, expected_response)

    def test_delete(self):
        client = RESTClient(TEST_API_KEY, TEST_API_SECRET)

        expected_response = {"key_1": "value_1", "key_2": "value_2"}

        with Mocker() as m:
            m.request(
                "DELETE",
                "https://api.coinbase.com/api/v3/brokerage/portfolios/1234",
                json=expected_response,
            )

            kwargs = {"test_kwarg": "test"}

            portfolio = client.delete("/api/v3/brokerage/portfolios/1234", **kwargs)

            captured_request = m.request_history[0]
            captured_headers = captured_request.headers

            self.assertEqual(captured_request.method, "DELETE")

            self.assertEqual(captured_request.json(), kwargs)

            self.assertTrue("User-Agent" in captured_headers)
            self.assertEqual(
                captured_headers["User-Agent"], "coinbase-advanced-py/" + __version__
            )
            self.assertTrue("Authorization" in captured_headers)
            self.assertTrue(captured_headers["Authorization"].startswith("Bearer "))

            self.assertEqual(portfolio, expected_response)

    def test_client_error(self):
        client = RESTClient(TEST_API_KEY, TEST_API_SECRET)

        with Mocker() as m:
            m.request(
                "GET",
                "https://api.coinbase.com/api/v3/brokerage/accounts",
                status_code=400,
            )

            with self.assertRaises(HTTPError):
                client.get("/api/v3/brokerage/accounts")

    def test_server_error(self):
        client = RESTClient(TEST_API_KEY, TEST_API_SECRET)

        with Mocker() as m:
            m.request(
                "GET",
                "https://api.coinbase.com/api/v3/brokerage/accounts",
                status_code=500,
            )

            with self.assertRaises(HTTPError):
                client.get("/api/v3/brokerage/accounts")

    def test_key_file_string(self):
        try:
            RESTClient(key_file="tests/test_api_key.json")
        except Exception as e:
            self.fail(f"An unexpected exception occurred: {e}")

    def test_key_file_object(self):
        try:
            key_file_object = StringIO(
                '{"name": "test-api-key-name","privateKey": "test-api-key-private-key"}'
            )
            RESTClient(key_file=key_file_object)
        except Exception as e:
            self.fail(f"An unexpected exception occurred: {e}")

    def test_key_file_no_key(self):
        with self.assertRaises(Exception):
            key_file_object = StringIO('{"field_1": "value_1","field_2": "value_2"}')
            RESTClient(key_file=key_file_object)

    def test_key_file_multiple_key_inputs(self):
        with self.assertRaises(Exception):
            key_file_object = StringIO('{"field_1": "value_1","field_2": "value_2"}')
            RESTClient(
                api_key=TEST_API_KEY,
                api_secret=TEST_API_SECRET,
                key_file=key_file_object,
            )

    def test_key_file_invalid_json(self):
        with self.assertRaises(Exception):
            key_file_object = StringIO(
                '"name": "test-api-key-name","privateKey": "test-api-key-private-key"'
            )
            RESTClient(key_file=key_file_object)
