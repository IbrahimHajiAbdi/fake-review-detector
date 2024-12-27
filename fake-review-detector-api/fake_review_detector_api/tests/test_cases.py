from django.test import TestCase
from django.test import Client


class TestCases(TestCase):
    def form_post(self):
        client = Client()
        response = client.post('/submit_form', {"review": "This is a test review."})
        self.assertRedirects(response, '/')
