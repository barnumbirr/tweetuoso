#!/usr/bin/env python
# -*- coding: utf-8 -*-

# I wrote this code as I needed a quick way to tweet the latest commits made to
# the Tweetuoso Github repository. This script has nothing to do with the Tweetuoso
# project per sei (even if it uses the tweepy module and the same auth files). 
# I just needed somewhere to store it safely.

# The tweet_commit function will not be added to Tweetuoso and probably won't be
# updated ever again as it works fine as it is.

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