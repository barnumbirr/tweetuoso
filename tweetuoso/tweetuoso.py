#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import cmd
import requests
import tweepy as tw
from auth import keys
from colorama import Fore, Style


def banner ():
  print(Fore.RED +
"""####################################################################
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
####################################################################\n""" +
		Fore.RESET)

def auth():
	print "Getting authorization url..."
	try:
		auth = tw.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
		try:
			url = auth.get_authorization_url()

		except tw.TweepError:
			print(Fore.RED + ">> " + Fore.RESET + "Error occured: Couldn't get token.")
			return

		print(Fore.RED + ">> " + Fore.RESET + "Please visit this url to get your access keys: \n" + url)
		pin = raw_input(Fore.RED + ">> " + Fore.RESET + "PIN: ").strip()
		auth.get_access_token(pin)
		print(Fore.RED + ">> " + Fore.RESET + "Add the following keys into the auth.py file :\n")
		print(Fore.RED + ">> " + Fore.RESET + "access_token = '%s'" % auth.access_token.key)
		print(Fore.RED + ">> " + Fore.RESET + "access_secret = '%s'" % auth.access_token.secret)

	except KeyboardInterrupt:
		print "\nAborted"

def auth_():
	""" Function doc """
	auth = tw.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
	auth.set_access_token(keys['access_token'], keys['access_secret'])
	api = tw.API(auth)
	return api

class TweetuosoCommands(cmd.Cmd):

	prompt = Fore.RED + ">> " + Fore.RESET

	def do_timeline(self, line):
		""" Show current timeline. """
		try:
			api = auth_()
			tl = api.home_timeline()
			for tweet in tl:
				print("   @" + Fore.RED + tweet.user.screen_name.encode('utf-8')
						+ Fore.RESET +
						tweet.created_at.strftime(
							Style.DIM +' tweeted on %d/%m/%Y at %H:%M\n' +
							Style.RESET_ALL) + "      " + tweet.text.encode('utf-8'))
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print(Fore.RED + ">> " + Fore.RESET + "Error occured: %s" % error)

	def do_mentions(self, line):
		""" Show tweets in which you were mentioned. """
		try:
			api = auth_()
			mt = api.mentions()
			for tweet in mt:
				print("   @" + Fore.RED + tweet.user.screen_name.encode('utf-8')
						+ Fore.RESET +
						tweet.created_at.strftime(
							Style.DIM +' tweeted you on %d/%m/%Y at %H:%M\n' +
							Style.RESET_ALL) + "      " + tweet.text.encode('utf-8'))
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print(Fore.RED + ">> " + Fore.RESET + "Error occured: %s" % error)

	def do_post(self, a):
		""" Post a tweet. """
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
					print(Fore.RED + ">> " + Fore.RESET + "Status updated successfully!")
				except requests.HTTPError:
					print(Fore.RED + ">> " + Fore.RESET + "Error: Unable to shorten URL.")
			else:
				api.update_status(a)
				print(Fore.RED + ">> " + Fore.RESET + "Status updated successfully!")
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print(Fore.RED + ">> " + Fore.RESET + "Error occured: %s" % error)

	def do_delete(self, tweet_id):
		""" Delete your tweet by given tweet_id. """
		try:
			api = auth_()
			api.destroy_status(tweet_id)
			print(Fore.RED + ">> " + Fore.RESET + "" + tweet_id + " deleted successfully.")
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print(Fore.RED + ">> " + Fore.RESET + "Error occured: %s" % error)

	def do_follow(self, user_id):
		""" Follow user with given user_id. """
		try:
			api = auth_()
			api.create_friendship(user_id)
			print(Fore.RED + ">> " + Fore.RESET + "You started following @" + Fore.RED + user_id + Fore.RESET +".")
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print(Fore.RED + ">> " + Fore.RESET + "Error occured: %s" % error)

	def do_unfollow(self, user_id):
		""" Unfollow user with given user_id. """
		try:
			api = auth_()
			api.destroy_friendship(user_id)
			print(Fore.RED + ">> " + Fore.RESET + "You successfully unfollowed @" + Fore.RED + user_id + Fore.RESET +".")
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print(Fore.RED + ">> " + Fore.RESET + "Error occured: %s" % error)

	def do_me(self, line):
		""" Show your profile information. """
		try:
			api = auth_()
			user = api.me()
			print("   @"+ Fore.RED + user.screen_name + Fore.RESET + " (" +
				Style.DIM + user.name + Style.RESET_ALL + ")\n      " +
				user.description + "\n      " + "Following: " +
				str(user.friends_count) + " || Followers: " +
				str(user.followers_count) + " || Tweets: " +
				str(user.statuses_count) + "|| Listed: " +
				str(user.listed_count) + "\n      " +
				user.location + " || " + user.url)
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print(Fore.RED + ">> " + Fore.RESET + "Error occured: %s" % error)

	def do_search(self, q):
		""" Search Twitter for <query> """
		try:
			api = auth_()
			src = api.search(q, rpp=20, result_type="recent")
			for tweet in src:
				print("   @"+ Fore.RED + tweet.from_user.encode('utf-8') +
						Fore.RESET +
						tweet.created_at.strftime(Style.DIM +
								' tweeted on %d/%m/%Y at %H:%M' + Style.RESET_ALL)
						+ "      " + tweet.text.encode('utf-8'))
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print(Fore.RED + ">> " + Fore.RESET + "Error occured: %s" % error)

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
			print(Fore.RED + ">> " + Fore.RESET + "Error occured: %s" % error)

	def do_stalk(self, q):
		""" Returns the last 20 tweets of given user."""
		""" If no user given return your latest tweets."""
		try:
			api = auth_()
			stk = api.user_timeline(q, count = 20, page = 1)
			for tweet in stk:
				print("   @"+ Fore.RED +
					tweet.user.screen_name.encode('utf-8') +
					Fore.RESET +
					tweet.created_at.strftime(Style.DIM +
							   ' tweeted on %d/%m/%Y at %H:%M\n' + Style.RESET_ALL)
					+ "      " + tweet.text.encode('utf-8'))
		except KeyboardInterrupt:
			print "\nAborted"
		except tw.TweepError as error:
			os.system('clear')
			print(Fore.RED + ">> " + Fore.RESET + "Error occured: %s" % error)
			
	def do_followback(self, line):
		""" Followback all your followers. """
		""" May be limited due to API rate limits. """
		""" Duration of operation depends on number of followers. """
		try:
			api = auth_()
			fol = api.followers()
			fri = api.friends()
			follow = [x for x in fol if x not in fri]
			print (Fore.RED + ">> " + Fore.RESET + "Working. This may take a while...")
			for u in follow:
				u.follow()
				print (Fore.RED + ">> " + Fore.RESET + 
					"You successfully followed back all of your followers.")
		except tw.TweepError as error:
			os.system('clear')
			print(Fore.RED + ">> " + Fore.RESET + "Error occured: %s" % error)
		print (Fore.RED + ">> " + Fore.RESET + "You successfully followed back all of your followers.")

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
		print "  +\tfollowback\t Followback all your followers.             +"
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
	if keys['access_token'] == '' and keys['access_secret'] == '':
		auth()
	else:
		main()
