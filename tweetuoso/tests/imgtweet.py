#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This won't work until the status_update_with_media() attribute is added to Tweepy API

__appname__ = 'imgtweet.py'
__version__ = "0.1"
__author__ = "c0ding"
__licence__ = "Apache v2.0 License"

import os
import sys
import tweepy as tw
from config import keys

def auth():
	api = tw.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
	api.set_access_token(keys['access_token'], keys['access_secret'])
	return api

def post():
	api = auth()
	picture = os.path.abspath(sys.argv[1])
	tweet = sys.argv[2]
	tw.api.status_update_with_media(picture, status=tweet)
	
if __name__ == '__main__':
	post()
