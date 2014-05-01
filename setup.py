#!/usr/bin/env python
#coding: utf-8

from distutils.core import setup

setup(
    name = 'tweetuoso',
    version = "1.0.5",
    url = "http://c0ding.github.com/tweetuoso/",
    download_url = "https://github.com/c0ding/tweetuoso/archive/master.zip",
    author = 'c0ding',
    author_email='me@martinsimon.me',
    license = "Apache v2.0 License",
    packages = ['tweetuoso'],
    description = 'Tweetuoso is a very light Twitter Command-line client developed in Python.',
    long_description = file('README.md','r').read(),
    keywords = 'twitter tweepy command-line tweetuoso',
    requires=[
        'colorama (==0.2.5)',
        'requests (==1.1.0)',
        'tweepy (==2.2)',
        'pytz',
    ],
)
