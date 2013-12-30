"""
Settings are all namespaced in the APPENGINE_TOOLKIT setting.
For example your project's `settings.py` file might look like this::

    APPENGINE_TOOLKIT = {
        'DEPENDENCIES_ROOT_NAME': 'libs',
    }

This module provides the `appengine_toolkit_settings` object, that is used to
access app's settings, checking for user settings first, then falling back to
the defaults.
"""
from __future__ import unicode_literals

from django.conf import settings

USER_SETTINGS = getattr(settings, 'APPENGINE_TOOLKIT', None)

DEFAULTS = {
    'APP_YAML': None,
    'DEPENDENCIES_ROOT': 'libs',
    'BUCKET_NAME': None,
}

# List of settings that cannot be empty
MANDATORY = (
    # absolute path to application file
    'APP_YAML',
)


class AppengineToolkitSettings(object):
    """
    A settings object, that allows settings to be accessed as properties.
    """

    def __init__(self, user_settings=None, defaults=None, mandatory=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or {}
        self.mandatory = mandatory or ()

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid Appengine Toolkit setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        self.validate_setting(attr, val)

        # Cache the result
        setattr(self, attr, val)
        return val

    def validate_setting(self, attr, val):
        if not val and attr in self.mandatory:
            raise AttributeError("Appengine Toolkit setting: '%s' is mandatory" % attr)


appengine_toolkit_settings = AppengineToolkitSettings(USER_SETTINGS, DEFAULTS, MANDATORY)
