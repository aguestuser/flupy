try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

CONFIG = {
    'description': 'My Project',
    'author': 'aguestuser',
    'url': 'Where to find the app',
    'download_url': 'where to download it',
    'author_email': 'aguestuser@riseup.net',
    'version': '0.0.1',
    'install_requires': ['nose'],
    'packages': ['fluent_python'],
    'scripts': [],
    'name': 'projectname'
}

setup(**CONFIG)
