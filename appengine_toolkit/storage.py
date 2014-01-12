from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
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
        """
        __init__ must be callable without arguments.
        Check for bucket name settings upon initialization
        """
        try:
            cloudstorage.validate_bucket_name(appengine_toolkit_settings.BUCKET_NAME)
        except ValueError:
            raise ImproperlyConfigured("Please specify a valid value for APPENGINE_TOOLKIT['BUCKET_NAME'] setting")
        self._bucket = '/' + appengine_toolkit_settings.BUCKET_NAME

    def path(self, name):
        """
        Returns the full path to the file, including leading '/' and bucket name.
        Access to the bucket root are not allowed.
        """
        if not name:
            raise SuspiciousOperation("Attempted access to '%s' denied." % name)
        return os.path.join(self._bucket, name)

    def _open(self, name, mode='rb'):
        return cloudstorage.open(self.path(name), 'r')

    def _save(self, name, content):
        realname = self.path(name)
        content_t = mimetypes.guess_type(realname)[0]
        with cloudstorage.open(realname, 'w', content_type=content_t, options={'x-goog-acl': 'public-read'}) as f:
            f.write(content.read())
        return os.path.join(self._bucket, realname)

    def delete(self, name):
        try:
            cloudstorage.delete(self.path(name))
        except cloudstorage.NotFoundError:
            pass

    def exists(self, name):
        try:
            cloudstorage.stat(self.path(name))
            return True
        except cloudstorage.NotFoundError:
            return False

    def listdir(self, name):
        return [], [obj.filename for obj in cloudstorage.listbucket(self.path(name))]

    def size(self, name):
        filestat = cloudstorage.stat(self.path(name))
        return filestat.st_size

    def url(self, name):
        key = blobstore.create_gs_key('/gs' + name)
        return images.get_serving_url(key)

    def created_time(self, name):
        filestat = cloudstorage.stat(self.path(name))
        creation_date = timezone.datetime.fromtimestamp(filestat.st_ctime)
        return timezone.make_aware(creation_date, timezone.get_current_timezone())

    def isdir(self, name):
        """
        TODO perform actual check, at the moment only happened Mezzanine calls this
        method
        """
        return True
