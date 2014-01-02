from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone

import os
import mimetypes

import cloudstorage
from google.appengine.ext import blobstore
from google.appengine.api import images

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

    def _realpath(self, name):
        return os.path.join(self._bucket, name) if name else self._bucket

    def _open(self, name, mode='rb'):
        return cloudstorage.open(os.path.join(self._bucket, name), 'r')

    def _save(self, name, content):
        realname = self._realpath(name)
        content_t = mimetypes.guess_type(realname)[0]
        with cloudstorage.open(realname, 'w', content_type=content_t, options={'x-goog-acl': 'public-read'}) as f:
            f.write(content.read())
        return os.path.join(self._bucket, realname)

    def delete(self, name):
        try:
            cloudstorage.delete(self._realpath(name))
        except cloudstorage.NotFoundError:
            pass

    def exists(self, name):
        try:
            cloudstorage.stat(self._realpath(name))
            return True
        except cloudstorage.NotFoundError:
            return False

    def listdir(self, path):
        return [], [obj.filename for obj in cloudstorage.listbucket(self._realpath(path))]

    def size(self, name):
        filestat = cloudstorage.stat(self._realpath(name))
        return filestat.st_size

    def url(self, name):
        key = blobstore.create_gs_key('/gs' + name)
        return images.get_serving_url(key)

    def created_time(self, name):
        filestat = cloudstorage.stat(self._realpath(name))
        return timezone.datetime.fromtimestamp(filestat.st_ctime)
