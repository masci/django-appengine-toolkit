from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils import timezone

from appengine_toolkit.storage import GoogleCloudStorage

from google.appengine.ext import testbed
import cloudstorage
import mock

import urlparse
import os


class TestStorage(TestCase):
    def setUp(self):
        self.storage = default_storage
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_urlfetch_stub()
        self.testbed.init_app_identity_stub()
        self.testbed.init_files_stub()
        self.testbed.init_blobstore_stub()
        cloudstorage.set_default_retry_params(None)
        # cleanup storage stub
        for elem in cloudstorage.listbucket('/test_bucket/'):
            cloudstorage.delete(elem.filename)

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
        self.assertTrue(self.storage.exists(path))
        # empty names are not allowed
        self.assertRaises(SuspiciousOperation, self.storage.exists, '')

    def test_file_created_time(self):
        cf = ContentFile('some contents')
        filename = self.storage.save('test.file', cf)
        now = timezone.now()
        ctime = self.storage.created_time(filename)
        self.assertTrue((now-ctime).seconds < 1)
        # empty names are not allowed
        self.assertRaises(SuspiciousOperation, self.storage.created_time, '')

    def test_delete(self):
        path = self.storage.save('test.txt', ContentFile('new content'))
        self.storage.delete(path)
        self.assertFalse(self.storage.exists('test.txt'))
        # empty names are not allowed
        self.assertRaises(SuspiciousOperation, self.storage.delete, '')

    def test_delete_nonexistent(self):
        self.storage.delete('fake.txt')

    def test_size(self):
        path = self.storage.save('test.txt', ContentFile('new content'))
        self.assertEqual(self.storage.size('test.txt'), 11)

    def test_listdir(self):
        self.storage.save('test.txt', ContentFile('a content'))
        self.storage.save('test.txt', ContentFile('another content'))
        files = self.storage.listdir(self.storage._bucket)[1]
        self.assertEqual(len(files), 2)

    def test_url(self):
        path = self.storage.save('test.txt', ContentFile('new content'))
        url = urlparse.urlparse(self.storage.url(path))
        self.assertTrue('_ah/img/' in url.path)

    def test_save(self):
        f = ContentFile('moar contents')
        path = self.storage.save('test.txt', f)
        with self.storage.open(path, 'r') as f:
            self.assertEqual(f.read(), 'moar contents')

    def test_file_save_without_name(self):
        """
        File storage extracts the filename from the content object if no
        name is given explicitly.
        """
        cf = ContentFile('contents')
        cf.name = 'foo_name.txt'
        path = self.storage.save(None, cf)
        self.assertEqual(path, os.path.join('/', self.storage._bucket, cf.name))