#!/usr/bin/env python
# -*- coding: utf-8 -*-

__appname__ = 'tweet_commit.py'
__version__ = "0.1"
__author__ = "c0ding"
__licence__ = "Apache v2.0 License"

import tweepy
from git import Repo
from config import keys
from colorama import Fore, Style

# Git repository path
git_path = 'repo_path'

def twitter_authorize():
	""" Function doc """
	auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
	auth.set_access_token(keys['access_token'], keys['access_secret'])
	api = tweepy.API(auth)
	return api


def tweet_commit():
	repo = Repo(git_path)
	assert repo.bare == False
	repo.config_reader()
	last_commit = repo.head.commit.message.strip("\n")
	api = twitter_authorize()
	tweet = "#Tweetuoso - The #Twitter Commandline client written in #Python updated: " + last_commit + " | http://is.gd/piWhzm"
	try:
		api.update_status(tweet)
		print "Last commit tweeted successfully!"
	except tweepy.TweepError as error:
		print("Error occured: " + Fore.RED + "%s" % error + Fore.RESET)

if __name__ == '__main__':
	tweet_commit()