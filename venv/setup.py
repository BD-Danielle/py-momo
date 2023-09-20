import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "selenium-crawler-momo",
    version = "0.1.0",
    description = ("selenium crawling automatically momo shopping site."),
    author = "YILING CHEN",
    author_email = "shutuzi88@gmail.com",
    packages = find_packages(),
    url = "https://github.com/shutuzi88/selenium-crawler",
    license = "LICENSE.txt",
    install_requires = required,
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    long_description = read('README.md')
)