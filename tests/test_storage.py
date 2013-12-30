from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import File, ContentFile
from django.core.files.storage import default_storage

from appengine_toolkit.storage import GoogleCloudStorage

from cloudstorage.errors import NotFoundError
from google.appengine.ext import testbed

import mock


class TestStorage(TestCase):
    def setUp(self):
        self.storage = default_storage
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_files_stub()
        self.testbed.init_blobstore_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_bucket_name(self):
        with mock.patch('appengine_toolkit.storage.appengine_toolkit_settings') as test_settings:
            test_settings.BUCKET_NAME = None
            self.assertRaises(ImproperlyConfigured, GoogleCloudStorage)
            test_settings.BUCKET_NAME = 'suitable'
            s = GoogleCloudStorage()
            self.assertIsInstance(s, GoogleCloudStorage)

    def test_exists(self):
        self.assertFalse(self.storage.exists('test.txt'))
        path = self.storage.save('test.txt', ContentFile('new content'))
