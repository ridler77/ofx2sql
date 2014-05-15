try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Isaac F Peterson',
    'url': 'https://github.com/ridler77/ofx2sql',
    'download_url': 'https://github.com/ridler77/ofx2sql/archive/master.zip',
    'author_email': 'isaac.f.peterson@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['ofx2sql'],
    'scripts': [],
    'name': 'ofx2sql'
}

setup(**config)