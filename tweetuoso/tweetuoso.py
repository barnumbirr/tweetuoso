#!/usr/bin/env python
# -*- coding: utf-8 -*-

__appname__ = 'tweetuoso'
__version__ = "1.0.1"
__author__ = "@c0ding <https://twitter.com/c0ding>"
__licence__ = "WTFPL"

import os
import re
import sys
import requests
import tweepy as tw

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''


def banner ():
  print """\033[31m####################################################################
##       _______                                                  ##
##      |__   __|                 _                               ##
##         | | __      _____  ___| |_ _   _  ___  ___  ___        ##
##         | | \ \ /\ / / _ \/ _ \ __| | | |/ _ \/ __|/ _ \       ##
##         | |  \ V  V /  __/  __/ |_| |_| | |_| \__ \ |_| |      ##
##         |_|   \_/\_/ \___|\___|\__|\____|\___/|___/\___/       ##
##                                                                ##
##                          ˈtwiːt[uoso]                          ##
##                                                                ##
##        The Twitter Commandline client written in Python        ##
##                                                                ##
##             Made with ♥ by @c0ding, February 2013              ##
##                      Licensed under WTFPL                      ##
####################################################################\n\033[0;0m"""

def auth():
	print "Getting authorization url..."
	try:
		auth = tw.OAuthHandler(consumer_key, consumer_secret)
		try:
			url = auth.get_authorization_url()

		except tw.TweepError:
			print "\033[31m>> \033[0;0mError occured, failed to get token\n"
			return

		print "\033[31m>> \033[0;0mPlease visit this url to get the token: \n" + url
		pin = raw_input('\033[31m>> \033[0;0mPIN: ').strip()
		auth.get_access_token(pin)
		print "\033[31m>> \033[0;0mPaste the following code to script's body:\n"
		print "\033[31m>> \033[0;0maccess_token = '%s'" % auth.access_token.key
		print "\033[31m>> \033[0;0maccess_secret = '%s'" % auth.access_token.secret

	except KeyboardInterrupt:
		print "\nAborted"

def auth_():
	""" Function doc """
	auth = tw.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tw.API(auth)
	return api

def timeline():
	try:
		api = auth_()
		tl = api.home_timeline()
		for tweet in tl:
			print "   @"+ "\033[31m"+ tweet.user.screen_name.encode('utf-8') + "\033[0;0m" + tweet.created_at.strftime(' \033[37mtweeted on %d/%m/%Y at %H:%M\033[0;0m\n') + "      " + tweet.text.encode('utf-8')
	except KeyboardInterrupt:
		print "\nAborted"
	except tw.TweepError:
		os.system('clear')
		print "\033[31m>> \033[0;0mError: Unable to perform action."

def mentions():
	try:
		api = auth_()
		mt = api.mentions()
		for tweet in mt:
			print "   @"+ "\033[31m"+ tweet.user.screen_name.encode('utf-8') + "\033[0;0m" + tweet.created_at.strftime(' \033[37mtweeted you on %d/%m/%Y at %H:%M\033[0;0m\n') + "      " + tweet.text.encode('utf-8')
	except KeyboardInterrupt:
		print "\nAborted"
	except tw.TweepError:
		os.system('clear')
		print "\033[31m>> \033[0;0mError: Unable to perform action."

def update(a):
	try:
		api = auth_()
		api.update_status(a)
		print "\033[31mStatus updated successfully!\033[0;0m"
	except KeyboardInterrupt:
		print "\nAborted"
	except tw.TweepError:
		print "\033[31m>> \033[0;0mError: Unable to perform action."

def destroy(tweet_id):
	""" Destroy your tweet by given tweet_id """
	try:
		api = auth_()
		api.destroy_status(tweet_id)
		print "\033[31m>> \033[0;0m" + tweet_id + " deleted successfully."
	except KeyboardInterrupt:
		print "\nAborted"
	except tw.TweepError:
		print "\033[31m>> \033[0;0mError: Unable to perform action."

def follow(user_id):
	""" Follow user with given user_id """
	try:
		api = auth_()
		api.create_friendship(user_id)
		print "You started following " + "\033[31m" + user_id + "\033[0;0m" +"."
	except KeyboardInterrupt:
		print "\nAborted"
	except tw.TweepError:
		print "\033[31m>> \033[0;0mError: Unable to perform action."

def unfollow(user_id):
	""" Unfollow user with given user_id """
	try:
		api = auth_()
		api.destroy_friendship(user_id)
		print "\033[31m>> \033[0;0mYou successfully unfollowed " + "\033[31m" + user_id + "\033[0;0m" +"."
	except KeyboardInterrupt:
		print "\nAborted"
	except tw.TweepError:
		print "\033[31m>> \033[0;0mError: Unable to perform action."

def me():
	try:
		api = auth_()
		user = api.me()
		print "   @"+ "\033[31m"+ user.screen_name + "\033[0;0m" + " (" + "\033[37m" + user.name + "\033[0;0m" + ")\n      " + user.description + "\n      " + "Following: " +  str(user.friends_count) + " || Followers: " + str(user.followers_count) + " || Tweets: " + str(user.statuses_count) + "\n      " + user.location + " || " + user.url
	except KeyboardInterrupt:
		print "\nAborted"
	except tw.TweepError:
		os.system('clear')
		print "\033[31m>> \033[0;0mError: Unable to perform action."

def search(q):
	try:
		api = auth_()
		src = api.search(q, rpp=20, result_type="recent")
		for tweet in src:
			print "   @"+ "\033[31m"+ tweet.from_user.encode('utf-8') + "\033[0;0m" + tweet.created_at.strftime(' \033[37mtweeted on %d/%m/%Y at %H:%M\033[0;0m\n') + "      " + tweet.text.encode('utf-8')
	except KeyboardInterrupt:
		print "\nAborted"
	except tw.TweepError:
		print "\033[31m>> \033[0;0mError: Unable to perform action."

def help():
	print "\033[31m   Menu:\n   ________________________________________________________________"
	print "   +                                                              +"
	print "   +\t1. Show timeline.                                         +"
	print "   +\t2. Show tweets that mentioned you.                        +"
	print "   +\t3. Post new tweet.                                        +"
	print "   +\t4. Delete tweet.                                          +"
	print "   +\t5. Me (Get account info).                                 +"
	print "   +\t6. Search for <query>.                                    +"
	print "   +\t7. Follow a new user.                                     +"
	print "   +\t8. Unfollow a user.                                       +"
	print "   +                                                              +"
	print "   +     Use 'quit' to leave.                                     +"
	print "   +______________________________________________________________+\033[0;0m"
	print ""

def main():
	banner()
	while True:
		try:
			x = raw_input('\033[31m>> \033[0;0m')

			if x == 'quit':
				os.system("clear")
				sys.exit(0)
			elif x == 'help':
				help()
			elif x == '1':
				timeline()
			elif x == '2':
				mentions()
			elif x == '3':
				status = raw_input("\033[31m>> \033[0;0mNew Tweet: ").strip()
				url = re.search("(?P<url>https?://[^\s]+)", status)
				if url is not None:
					try:
						long_url = url.group("url")
						short_url = "http://is.gd/create.php?format=simple&url=" + long_url
						r = requests.get(short_url)
						status = status.replace(long_url, r.text)
						update(status)
					except requests.HTTPError:
						print "\033[31m>> \033[0;0mError: Unable to shorten URL."
			elif x == '4':
				d = raw_input('\033[31m>> \033[0;0mTweet ID: ')
				destroy(d)
			elif x == '5':
				me()
			elif x == '6':
				q = raw_input('\033[31m>> \033[0;0mSearch for: ')
				search(q)
			elif x == '7':
				u = raw_input('\033[31m>> \033[0;0mUser you wish to follow: ')
				follow(u)
			elif x == '8':
				u = raw_input('\033[31m>> \033[0;0mUser you wish to unfollow: ')
				unfollow(u)
			else:
				help()
		except EOFError:
			os.system("clear");
			help()
		except KeyboardInterrupt:
			print "\033[31m>>\033[0;0m Use 'quit' to leave."

if __name__ == '__main__':
	os.system('clear')
	if access_token == '' and access_secret == '':
		auth()
	else:
		main()
