__version__ = '0.2.1'

import os

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

DEFAULT_ENV = 'DATABASE_URL'

# Register database schemes in URLs.
urlparse.uses_netloc.append('mysql')
urlparse.uses_netloc.append('rdbms')

SCHEMES = {
    'mysql': 'django.db.backends.mysql',
    'rdbms': 'google.appengine.ext.django.backends.rdbms',
}


def on_appengine():
    """
    Determine if program is running on App Engine servers
    """
    return os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine')


def config(env=DEFAULT_ENV, default=None):
    """
    Returns configured DATABASE dictionary from DEFAULT_ENV.
    """
    config = {}

    s = os.environ.get(env, default)

    if s:
        config = parse(s)

    return config


def parse(url):
    """
    Parses a database URL in this format:
    [database type]://[username]:[password]@[host]:[port]/[database name]

    or, for cloud SQL:
    [database type]://[username]:[password]@[project_id]:[instance_name]/[database name]
    """
    config = {}

    url = urlparse.urlparse(url)

    # Remove query strings.
    path = url.path[1:]
    path = path.split('?', 2)[0]

    try:
        port = url.port
        hostname = url.hostname
    except ValueError:
        port = None
        if url.scheme == 'rdbms':
            # local appengine stub requires INSTANCE parameter
            config['INSTANCE'] = url.netloc.split('@')[-1]
            hostname = None
        else:
            hostname = "/cloudsql/{}".format(url.netloc.split('@')[-1])

    config.update({
        'NAME': path,
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': hostname,
        'PORT': port,
    })

    if url.scheme in SCHEMES:
        config['ENGINE'] = SCHEMES[url.scheme]

    return config