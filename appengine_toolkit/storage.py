from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured

from oauth2client.client import OAuth2WebServerFlow
from oauth2client import clientsecrets

from .settings import appengine_toolkit_settings


def flow_from_settings():
    """

    """
    scope = appengine_toolkit_settings.SCOPE
    client_type = appengine_toolkit_settings.CLIENT_TYPE
    if client_type in (clientsecrets.TYPE_WEB, clientsecrets.TYPE_INSTALLED):
        constructor_kwargs = {
            'redirect_uri': appengine_toolkit_settings.REDIRECT_URI,
            'auth_uri': appengine_toolkit_settings.AUTH_URI,
            'token_uri': appengine_toolkit_settings.TOKEN_URI,
        }
        revoke_uri = appengine_toolkit_settings.REVOKE_URI
        if revoke_uri is not None:
            constructor_kwargs['revoke_uri'] = revoke_uri
        return OAuth2WebServerFlow(appengine_toolkit_settings.CLIENT_ID, appengine_toolkit_settings.CLIENT_SECRET,
                                   scope, **constructor_kwargs)


class GoogleCloudStorage(Storage):
    """

    """
    def __init__(self):
        pass

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content):
        pass

    def delete(self, name):
        pass

    def exists(self, name):
        pass

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


