#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy as tw
from config import keys
from colorama import Fore, Style
 
class Listener(tw.StreamListener):
	
	def on_status(self, tweet):
		tweet.text = tweet.text.replace("\n", " ")
		print("   @" + Fore.RED + tweet.author.screen_name.encode('utf-8')
						+ Fore.RESET +
						tweet.created_at.strftime(
							Style.DIM +' tweeted on %d/%m/%Y at %H:%M' +
							Style.RESET_ALL) + "\n      " + tweet.text.encode('utf-8'))

					
def auth():
		
	api = tw.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
	api.set_access_token(keys['access_token'], keys['access_secret'])
	return api

if __name__ == '__main__':
	api = auth()
	streaming_api = tw.streaming.Stream(api, Listener(), timeout=60)
	streaming_api.filter(follow=None, track=['GTA 5'])
