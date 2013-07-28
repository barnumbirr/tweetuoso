#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import cmd
import pytz
import codecs
import requests
import tweepy as tw
from config import keys
from config import settings
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
##                                                  v.1.0.4       ##
##                          ˈtwiːt[uoso]                          ##
##                                                                ##
##        The Twitter Command-line client written in Python       ##
##                                                                ##
##             Made with ♥ by @c0ding, February 2013              ##
##                Licensed under Apache v2 License                ##
####################################################################\n""" +
Fore.RESET)

def prompt_print(text):
	""" Simple prompt funtion. """
	""" Makes it a bit cleaner and maintainable if the prompt ever needs to change. """
	print(Fore.RED + ">> " + Fore.RESET + text)

def auth():
	""" Initializes Tweetuoso for the first time. """
	""" Checks for valid Twitter API keys. """
	banner()
	prompt_print("Getting authorization URL...")
	try:
		auth = tw.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
		try:
			url = auth.get_authorization_url()
		except tw.TweepError:
			prompt_print("Error occured: Couldn't get token.")
			return

		prompt_print("Please visit this url to get your access keys:")
		prompt_print(url)
		pin = raw_input(Fore.RED + ">> " + Fore.RESET + "PIN: ").strip()
		try:
			auth.get_access_token(pin)
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)
			return
		prompt_print("Add the following keys into the config.py file :")
		prompt_print("access_token = '%s'" % auth.access_token.key)
		prompt_print("access_secret = '%s'" % auth.access_token.secret)

	except KeyboardInterrupt:
		os.system("clear")
		sys.exit(0)

def auth_():
	""" Function doc """
	auth = tw.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
	auth.set_access_token(keys['access_token'], keys['access_secret'])
	api = tw.API(auth)
	return api

class TweetuosoCommands(cmd.Cmd):

	prompt = Fore.RED + ">> " + Fore.RESET

	def emptyline(self):
		""" Return empty line instead of repeating last command. """
		pass

	def default(self, inp):
		""" Return error if <input> is not a valid command. """
		print "'" + inp + "'" + " is not a valid command. Try using 'help'."

	def do_timeline(self, line):
		""" Show current timeline. """
		try:
			api = auth_()
			tl = api.home_timeline()
			if settings['reversed_timeline'] == True:
				tl.reverse()
			for tweet in tl:
				tweet.text = tweet.text.replace("\n", " ")
				print("   @" + Fore.RED + tweet.user.screen_name.encode('utf-8')
						+ Fore.RESET +
						tweet.created_at.strftime(
							Style.DIM +' tweeted on %d/%m/%Y at %H:%M' + Style.RESET_ALL) + "\n      " +
							tweet.text.encode('utf-8') + "\n      " + 'http://twitter.com/'+tweet.author.screen_name.encode('utf-8')+'/status/'+str(tweet.id))
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)

	def do_mentions(self, line):
		""" Show tweets in which you were mentioned. """
		try:
			api = auth_()
			mt = api.mentions_timeline()
			if settings['reversed_mentions'] == True:
				mt.reverse()
			for tweet in mt:
				tweet.text = tweet.text.replace("\n", " ")
				print("   @" + Fore.RED + tweet.user.screen_name.encode('utf-8')
						+ Fore.RESET +
						tweet.created_at.strftime(
							Style.DIM +' tweeted on %d/%m/%Y at %H:%M' +
							Style.RESET_ALL) + "\n      " + tweet.text.encode('utf-8'))
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)

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
					prompt_print("Status updated successfully!")
				except requests.HTTPError:
					prompt_print("Error: Unable to shorten URL.")
			else:
				api.update_status(a)
				prompt_print("Status updated successfully!")
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)

	def do_delete(self, tweet_id):
		""" Delete your tweet by given tweet_id. """
		try:
			api = auth_()
			api.destroy_status(tweet_id)
			prompt_print(tweet_id + " deleted successfully.")
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)

	def do_follow(self, user_id):
		""" Follow user with given user_id. """
		try:
			api = auth_()
			api.create_friendship(user_id)
			prompt_print("You started following @" + Fore.RED + user_id + Fore.RESET +".")
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)

	def do_unfollow(self, user_id):
		""" Unfollow user with given user_id. """
		try:
			api = auth_()
			api.destroy_friendship(user_id)
			prompt_print("You successfully unfollowed @" + Fore.RED + user_id + Fore.RESET +".")
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)

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
				user.location + " || " + str(user.url))
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)

	def do_search(self, q):
		""" Search Twitter for <query> """
		try:
			api = auth_()
			src = api.search(q, rpp=20, result_type="recent")
			for tweet in src:
				tweet.text = tweet.text.replace("\n", " ")
				print("   @"+ Fore.RED + tweet.user.screen_name.encode('utf-8') +
						Fore.RESET +
						tweet.created_at.strftime(Style.DIM +
								' tweeted on %d/%m/%Y at %H:%M' + Style.RESET_ALL)
						+ "\n      " + tweet.text.encode('utf-8'))
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)
			
	def do_trends(self, line):
		""" Returns the top 10 trending topics for the day. """
		""" WOEID list available at http://developer.yahoo.com/geo/geoplanet/"""
		try:
			api = auth_()
			t = api.trends_place(settings['WOEID'])
			trends = "  " + "\n  ".join(i["name"] for i in t[0]["trends"])
			print trends.encode('utf-8')
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)

	def do_stalk(self, q):
		""" Returns the last 20 tweets of given user."""
		""" If no user given return your latest tweets."""
		try:
			api = auth_()
			stk = api.user_timeline(q, count = 20, page = 1)
			if settings['reversed_stalk'] == True:
				stk.reverse()
			for tweet in stk:
				tweet.text = tweet.text.replace("\n", " ")
				print("   @"+ Fore.RED +
					tweet.user.screen_name.encode('utf-8') +
					Fore.RESET +
					tweet.created_at.strftime(Style.DIM +
							   ' tweeted on %d/%m/%Y at %H:%M' + Style.RESET_ALL)
					+ "\n      " + tweet.text.encode('utf-8'))
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)

	def do_followback(self, line):
		""" Followback all your followers. """
		""" May be limited due to API rate limits. """
		""" Duration of operation depends on number of followers. """
		try:
			api = auth_()
			fol = api.followers()
			fri = api.friends()
			follow = [x for x in fol if x not in fri]
			prompt_print ("Working. This may take a while...")
			for u in follow:
				u.follow()
				prompt_print ("You successfully followed back all of your followers.")
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)
			
	def do_retweet(self, tweet_id):
		""" Retweet a tweet by given tweet_id. """
		try:
			api = auth_()
			retweet = api.retweet(tweet_id)
			tweet = retweet
			tweet.text = tweet.text.replace("\n", " ")
			print("   @"+ Fore.RED +
				tweet.user.screen_name.encode('utf-8') +
				Fore.RESET +
				tweet.created_at.strftime(Style.DIM +
						   ' tweeted on %d/%m/%Y at %H:%M' + Style.RESET_ALL)
				+ "\n      " + tweet.text.encode('utf-8'))
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)
			
			
	def do_archive(self, line):
		""" Archive your tweets to a .txt file. """
		""" May be limited due to API rate limits. """
		""" Duration of operation depends on number of tweets. """
		try:
			utc = pytz.utc
			homeTZ = pytz.timezone(settings['timezone'])
			status_list = []
			cur_status_count = 0 
			api = auth_()
			statuses = api.user_timeline(count=200, include_rts=True)
			theUser = statuses[0].author
			total_status_count = theUser.statuses_count
			archivefile = settings['archive_path'] + theUser.screen_name + "'s_tweets.txt"
			prompt_print("Archiving @" + Fore.RED + theUser.screen_name + Fore.RESET + "'s tweets to " + archivefile)
			while statuses != []:
				cur_status_count = cur_status_count + len(statuses)
				for status in statuses:
					status_list.append(status)
					theMaxId = statuses[-1].id
					theMaxId = theMaxId - 1
				statuses = api.user_timeline(count=200, include_rts=True, max_id=theMaxId)
				prompt_print("%d of %d tweets processed..." % (cur_status_count, total_status_count))
			prompt_print("Total Statuses Retrieved: " + Fore.RED + str(len(status_list)) + Fore.RESET)
			prompt_print("Writing statuses to log file...")
			f = codecs.open(archivefile, 'a', 'utf-8')
			if settings['reversed_archive'] == True:
							status_list.reverse()
			for status in status_list:
				theTime = utc.localize(status.created_at).astimezone(homeTZ)
				f.write('@'+ status.author.screen_name + ' tweeted on ' + theTime.strftime("%d/%m/%Y at %H:%M\n"))
				f.write('      ' + status.text)
				f.write('\n      ' + 'http://twitter.com/'+status.author.screen_name+'/status/'+str(status.id)+'\n')
				f.write('- - - - - - - -\n\n')
			f.close()
			prompt_print("You successfully archived all of your tweets!")
		except tw.TweepError as error:
			prompt_print("Error occured: %s" % error)

	def do_help(self, line):
		""" Show detailed help. """
		print Fore.RED + "   Commands:\n   _________________________________________________________________"
		print "  +                                                                 +"
		print "  +\ttimeline\t Show public timeline.                      +"
		print "  +\tmentions\t Show tweets that mentioned you.            +"
		print "  +\tstalk\t\t Show <user> timeline                       +"
		print "  +\tpost\t\t Post new tweet.                            +"
		print "  +\tdelete\t\t Delete tweet.                              +"
		print "  +\tretweet\t\t Retweet tweet.                             +"
		print "  +\tme\t\t Me (Get account info).                     +"
		print "  +\tsearch\t\t Search for <query>.                        +"
		print "  +\tfollow\t\t Follow a new user.                         +"
		print "  +\tunfollow\t Unfollow a user.                           +"
		print "  +\tfollowback\t Followback all your followers.             +"
		print "  +\tarchive\t\t Save all your tweets to a text file.       +"
		print "  +\ttrends\t\t Show today's trends.                       +"
		print "  +                                                                 +"
		print "  +     Use 'quit' or 'exit' to leave.                              +"
		print "  +_________________________________________________________________+" + Fore.RESET
		print ""
		
	def do_quit(self, line):
		os.system("clear")
		sys.exit(0)
	
	def do_exit(self, line):
		os.system("clear")
		sys.exit(0)

def main():
	try:
		banner()
		TweetuosoCommands().cmdloop()
	except KeyboardInterrupt:
		os.system("clear")
		sys.exit(0)

if __name__ == '__main__':
	os.system('clear')
	if keys['access_token'] == '' and keys['access_secret'] == '':
		auth()
	else:
		main()
