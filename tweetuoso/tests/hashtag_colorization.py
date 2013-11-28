#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Testing hashtag colorization. This should be implemented in v.1.0.5 of Tweetuoso but
# I have to figure out how to use this in the best possible way first...

__appname__ = 'hashtag_colorization.py'
__version__ = "0.1"
__author__ = "c0ding"
__licence__ = "Apache v2.0 License"

from colorama import Fore, Style

tweet = "This is an #awesome example #string to test #hashtag colors."

def highlight(hashtag):
	for word in tweet.split():
		if word.startswith("#"):
			print Fore.RED + word + Fore.RESET,
		else:
			print word,
			
if __name__ == '__main__':
	highlight(tweet)