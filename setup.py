#!/usr/bin/env python
#coding: utf-8

from setuptools import setup, find_packages

setup(
    name = 'tweetuoso',
    version = "1.0.1",
    url = "http://c0ding.github.com/tweetuoso/",
    download_url = "https://github.com/c0ding/tweetuoso/archive/master.zip",
    author = 'c0ding',
    license = "WTFPL",
    packages = find_packages(),
    description = 'Tweetuoso is a very light Twitter Command-line client developed in Python.',
    long_description=open('README.md').read(),
    keywords = 'twitter tweepy python command-line',
    scripts = ['tweetuoso/tweetuoso.py']
)
