#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import cmd
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

		except tw.TweepError as error:
			print "\033[31m>> \033[0;0mError occured: " + str(error)
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

class TweetuosoCommands(cmd.Cmd):

	prompt = "\033[31m>> \033[0;0m"

	def do_timeline(self, line):
		""" Show current timeline """
		try:
			api = auth_()
			tl = api.home_timeline()
			for tweet in tl:
				print "   @"+ "\033[31m"+ tweet.user.screen_name.encode('utf-8') + "\033[0;0m" + tweet.created_at.strftime(' \033[37mtweeted on %d/%m/%Y at %H:%M\033[0;0m\n') + "      " + tweet.text.encode('utf-8')
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print "\033[31m>> \033[0;0mError occured: " + str(error)

	def do_mentions(self, line):
		""" Show tweets in which you were mentioned """
		try:
			api = auth_()
			mt = api.mentions()
			for tweet in mt:
				print "   @"+ "\033[31m"+ tweet.user.screen_name.encode('utf-8') + "\033[0;0m" + tweet.created_at.strftime(' \033[37mtweeted you on %d/%m/%Y at %H:%M\033[0;0m\n') + "      " + tweet.text.encode('utf-8')
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print "\033[31m>> \033[0;0mError occured: " + str(error)

	def do_post(self, a):
		""" Post a tweet """
		try:
			api = auth_()
			url = re.search("(?P<url>https?://[^\s]+)", a)
			if url is not None:
				try:
					long_url = url.group("url")
					short_url = "http://is.gd/create.php?format=simple&url=" + long_url
					r = requests.get(short_url)
					a = a.replace(long_url, r.text)
					api.update_status(a)
					print "\033[31m>> \033[0;0mStatus updated successfully!\033[0;0m"
				except requests.HTTPError:
					print "\033[31m>> \033[0;0mError: Unable to shorten URL."
			else:
				api.update_status(a)
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print "\033[31m>> \033[0;0mError occured: " + str(error)

	def do_delete(self, tweet_id):
		""" Delete your tweet by given tweet_id """
		try:
			api = auth_()
			api.destroy_status(tweet_id)
			print "\033[31m>> \033[0;0m" + tweet_id + " deleted successfully."
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print "\033[31m>> \033[0;0mError occured: " + str(error)

	def do_follow(self, user_id):
		""" Follow user with given user_id """
		try:
			api = auth_()
			api.create_friendship(user_id)
			print "\033[31m>> \033[0;0mYou started following @" + "\033[31m" + user_id + "\033[0;0m" +"."
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print "\033[31m>> \033[0;0mError occured: " + str(error)

	def do_unfollow(self, user_id):
		""" Unfollow user with given user_id """
		try:
			api = auth_()
			api.destroy_friendship(user_id)
			print "\033[31m>> \033[0;0mYou successfully unfollowed @" + "\033[31m" + user_id + "\033[0;0m" +"."
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print "\033[31m>> \033[0;0mError occured: " + str(error)

	def do_me(self, line):
		""" Show your profile information """
		try:
			api = auth_()
			user = api.me()
			print "   @"+ "\033[31m"+ user.screen_name + "\033[0;0m" + " (" + "\033[37m" + user.name + "\033[0;0m" + ")\n      " + user.description + "\n      " + "Following: " +  str(user.friends_count) + " || Followers: " + str(user.followers_count) + " || Tweets: " + str(user.statuses_count) + "|| Listed: " + str(user.listed_count) + "\n      " + user.location + " || " + user.url
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print "\033[31m>> \033[0;0mError occured: " + str(error)

	def do_search(self, q):
		""" Search Twitter """
		try:
			api = auth_()
			src = api.search(q, rpp=20, result_type="recent")
			for tweet in src:
				print "   @"+ "\033[31m"+ tweet.from_user.encode('utf-8') + "\033[0;0m" + tweet.created_at.strftime(' \033[37mtweeted on %d/%m/%Y at %H:%M\033[0;0m\n') + "      " + tweet.text.encode('utf-8')
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print "\033[31m>> \033[0;0mError occured: " + str(error)

	def do_trends(self, line):
		""" Returns the top 20 trending topics for the day. """
		try:
			api = auth_()
			t = api.trends_location(1)
			trends = "\n".join(i["name"] for i in t[0]["trends"])
			print trends
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print "\033[31m>> \033[0;0mError occured: " + str(error)

	def do_stalk(self, q):
		""" Returns the last 20 tweets of given user."""
		""" If no user given return your latest tweets."""
		try:
			api = auth_()
			stk = api.user_timeline(q, count = 20, page = 1)
			for tweet in stk:
				print "   @"+ "\033[31m"+ tweet.user.screen_name.encode('utf-8') + "\033[0;0m" + tweet.created_at.strftime(' \033[37mtweeted on %d/%m/%Y at %H:%M\033[0;0m\n') + "      " + tweet.text.encode('utf-8')
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print "\033[31m>> \033[0;0mError occured: " + str(error)
			
	def do_quit(self, line):
		os.system("clear")
		sys.exit(0)
		
	def do_help(self, line):
		""" Show detailed help """
		print "\n\033[31m   Commands:\n   _________________________________________________________________"
		print "  +                                                                 +"
		print "  +\ttimeline\t Show public timeline.                      +"
		print "  +\tmentions\t Show tweets that mentioned you.            +"
		print "  +\tstalk\t\t Show <user> timeline                       +"
		print "  +\tpost\t\t Post new tweet.                            +"
		print "  +\tdelete\t\t Delete tweet.                              +"
		print "  +\tme\t\t Me (Get account info).                     +"
		print "  +\tsearch\t\t Search for <query>.                        +"
		print "  +\tfollow\t\t Follow a new user.                         +"
		print "  +\tunfollow\t Unfollow a user.                           +"
		print "  +\ttrends\t\t Show today's trends.                       +"
		print "  +                                                                 +"
		print "  +     Use 'quit' to leave.                                        +"
		print "  +_________________________________________________________________+\033[0;0m"
		print ""


def main():
	banner()
	TweetuosoCommands().cmdloop()


if __name__ == '__main__':
	os.system('clear')
	if access_token == '' and access_secret == '':
		auth()
	else:
		main()
