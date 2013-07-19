#!/usr/bin/env python
# -*- coding: utf-8 -*-

__appname__ = 'streaming'
__version__ = "0.1"
__author__ = "c0ding"
__licence__ = "Apache v2 License"

import os
import sys
import tweepy as tw
from config import keys
from colorama import Fore, Style

def auth():
		
	api = tw.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
	api.set_access_token(keys['access_token'], keys['access_secret'])
	return api
 
class Listener(tw.StreamListener):
	
	def on_status(self, tweet):
		tweet.text = tweet.text.replace("\n", " ")
		print("   @" + Fore.RED + tweet.author.screen_name.encode('utf-8')
						+ Fore.RESET +
						tweet.created_at.strftime(
							Style.DIM +' tweeted on %d/%m/%Y at %H:%M' +
							Style.RESET_ALL) + "\n      " + tweet.text.encode('utf-8'))
							
	def on_error(self, status_code):
		print "Error occured: %s" % status_code

def streaming():
	try:
		api = auth()
		mode = raw_input("Which streaming mode do you want? [sample/filter]? ")
		if mode == 'sample':
			stream = tw.streaming.Stream(api, Listener(), timeout=60)
			stream.sample()
		if mode == 'filter':
			track_list = raw_input('Keywords to track (comma separated): ')
			','.join(track_list)
			stream = tw.streaming.Stream(api, Listener(), timeout=60)
			stream.filter(follow=None, track=[track_list])
	except KeyboardInterrupt:
		os.system("clear")
		stream.disconnect()
		
if __name__ == '__main__':
	streaming()
