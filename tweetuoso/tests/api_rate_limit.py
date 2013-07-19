#!/usr/bin/env python
# -*- coding: utf-8 -*-

__appname__ = 'api_rate_limit'
__version__ = "0.3"
__author__ = "c0ding"
__licence__ = "Apache v2 License"

import os
import tweepy as tw
from config import keys
from colorama import Fore, Style

def rate_limit():
	try:
		auth = tw.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
		auth.set_access_token(keys['access_token'], keys['access_secret'])
		api = tw.API(auth)
		print api.rate_limit_status()
		
	except tw.TweepError as error:
		os.system('clear')
		print(Fore.RED + ">> " + Fore.RESET + "Error occured: %s" % error)
		return
					
if __name__ == '__main__':
	rate_limit()