from django.test import TestCase

from appengine_toolkit.storage import GoogleCloudStorage


class TestStorage(TestCase):
    def test_bo(self):
        s = GoogleCloudStorage()

