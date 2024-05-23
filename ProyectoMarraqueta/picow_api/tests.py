from django.test import TestCase
from django.http import HttpRequest

from . import views as api_views

class CommunicationTests(TestCase):
    def test_recv_not_post_request(self):
        request = HttpRequest()
        request.method="GET"
        response = api_views.recv(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.closed, True)
