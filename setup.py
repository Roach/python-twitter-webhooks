from setuptools import setup
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

setup(name='twitterwebhooks',
      version='1.0.0',
      description='Python Twitter Webhooks',
      url='http://github.com/roach/python-twitter-webhooks',
      author='@roach',
      author_email='roach@roach.wtf',
      license='MIT',
      packages=['twitterwebhooks'],
      install_requires=[
        'flask',
        'pyee',
        'requests',
      ],
      zip_safe=False)
