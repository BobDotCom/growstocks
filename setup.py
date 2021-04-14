import codecs
import os.path
import re

import setuptools


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


# The full version, including alpha/beta/rc tags
with open('growstocks/__init__.py') as f:
    __version__ = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1) or ''

with open("README.rst", "r") as fh:
    long_description = fh.read().replace("""===================
growstocks
===================""", """===================
growstocks {0}
===================""".format(__version__))

setuptools.setup(
    name="growstocks",
    version=__version__,
    author="BobDotCom",
    author_email="bobdotcomgt@gmail.com",
    description="A wrapper for the GrowStocks API, made for both synchronous and asynchronous applications.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/BobDotCom/growstocks",
    download_url='https://github.com/BobDotCom/growstocks/releases',
    packages=setuptools.find_packages(exclude=['tests*', 'build.py']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        ],
    python_requires='>=3.5',
    install_requires=[
            'requests',
            'urllib3',
            'aiohttp'
        ],
    license='MIT',
    project_urls={
        'Documentation': 'https://growstocks.readthedocs.io/en/latest/index.html',
        'Source':        'https://github.com/BobDotCom/growstocks',
        'Tracker':       'https://github.com/BobDotCom/growstocks/issues'
        }
    )
