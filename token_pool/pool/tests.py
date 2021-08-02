from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.test import RequestsClient


class TestTokenPoolView(APITestCase):
    """
    Test the TokenPoolView list from api.
    """

    def setUp(self) -> None:
        # Calling Loan request factory from LeadFactory
        self.host = 'http://127.0.0.1:8000'
        self.client = RequestsClient()

    def test_token_journey(self):
        """Test whole token flow."""
        # Calling the API
        url = self.host + reverse('pool-token')
        response = self.client.post(url)
        resp = response.json()

        # Testing the response
        self.assertTrue(resp['token'])

        url = self.host + reverse('block-token')
        response = self.client.post(url)
        resp = response.json()
        token = resp.get('blocked_token')

        # Testing the response
        self.assertTrue(resp['blocked_token'])

        url = self.host + reverse('keep-alive', args=(token,))
        response = self.client.post(url)
        resp = response.json()

        # Testing the response
        self.assertTrue(resp['response'])

        url = self.host + reverse('pool-token')
        data = {'token_uuid': token}
        response = self.client.delete(url, json=data)
        resp = response.json()

        # Testing the response
        self.assertTrue(resp['response'])

    def test_token_not_available(self):
        """Test token when its not available."""
        # Calling the API
        url = self.host + reverse('pool-token')
        response = self.client.post(url)
        resp = response.json()

        # Testing the response
        self.assertTrue(resp['token'])

        url = self.host + reverse('block-token')
        response = self.client.post(url)
        resp = response.json()
        # token = resp.get('blocked_token')

        # Testing the response
        self.assertTrue(resp['blocked_token'])

        url = self.host + reverse('block-token')
        response = self.client.post(url)
        resp = response.json()

        # Testing the response
        self.assertTrue(resp['error'])
