#!/usr/bin/env python
# -*- coding: utf-8 -*-

__appname__ = 'api_rate_limit'
__version__ = "0.1a"
__author__ = "@c0ding <https://twitter.com/c0ding>"
__licence__ = "WTFPL"

import tweepy as tw

consumer_key = 'm4S43wXKmfWR31lgwzRJg'
consumer_secret = 'nZwQYsGXa7Vg7KBltf6aw8ao3GV8ltCTPjje4Rwrr6k'
access_token = '636598354-pfEmyHsAR9FuUVVv3uEdkdepB5gsuo7CcizZiV7Y' 
access_secret = 'Os6RDzY7ufE3hp8pL7gGbUFfHOniGMzs9s3Ae3BYE3o'

def rate_limit():
	auth = tw.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tw.API(auth)
	print api.rate_limit_status()

if __name__ == '__main__':
	rate_limit()