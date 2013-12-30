from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured

import os
import mimetypes

import cloudstorage

from .settings import appengine_toolkit_settings


class GoogleCloudStorage(Storage):
    """

    """
    def __init__(self):
        try:
            cloudstorage.validate_bucket_name(appengine_toolkit_settings.BUCKET_NAME)
        except ValueError:
            raise ImproperlyConfigured("Please specify a valid value for APPENGINE_TOOLKIT['BUCKET_NAME'] setting")
        self._bucket = '/' + appengine_toolkit_settings.BUCKET_NAME

    def _open(self, name, mode='rb'):
        return cloudstorage.open(os.path.join(self._bucket, name), 'r')

    def _save(self, name, content):
        filename = os.path.join(self._bucket, name)
        content_t = mimetypes.guess_type(filename)[0]
        with cloudstorage.open(filename, 'w', content_type=content_t, options={'x-goog-acl': 'public-read'}) as handle:
            handle.write(content.read())
        return os.path.join(self._bucket, filename)

    def delete(self, name):
        pass

    def exists(self, name):
        try:
            cloudstorage.stat(os.path.join(self._bucket, name))
            return True
        except cloudstorage.NotFoundError:
            return False

    def listdir(self, path):
        pass

    def size(self, name):
        pass

    def url(self, name):
        pass

    def accessed_time(self, name):
        pass

    def created_time(self, name):
        pass

    def modified_time(self, name):
        pass


