#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytz
import codecs
import tweepy as tw
from config import keys

utc = pytz.utc
archiveFile = "/Users/c0ding/Desktop/twitter.txt"
homeTZ = pytz.timezone('Europe/Paris')

def auth():
		
	auth = tw.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
	auth.set_access_token(keys['access_token'], keys['access_secret'])
	api = tw.API(auth)
	return api

status_list = []
cur_status_count = 0 

api = auth()
statuses = api.user_timeline(count=200, include_rts=True)
theUser = statuses[0].author
total_status_count = theUser.statuses_count
print "Archiving " + theUser.name + "'s tweets to " + archiveFile

while statuses != []:
    cur_status_count = cur_status_count + len(statuses)
    for status in statuses:
        status_list.append(status)
    
    # Get tweet id from last status in each page
    theMaxId = statuses[-1].id
    theMaxId = theMaxId - 1
    
    # Get new page of statuses based on current id location
    statuses = api.user_timeline(count=200, include_rts=True, max_id=theMaxId)
    print "%d of %d tweets processed..." % (cur_status_count, total_status_count)

print "Total Statuses Retrieved: " + str(len(status_list))
print "Writing statuses to log file:"

f = codecs.open(archiveFile, 'a', 'utf-8')
for status in reversed(status_list):
    theTime = utc.localize(status.created_at).astimezone(homeTZ)
    f.write(status.text + '\n')
    f.write(theTime.strftime("%d/%m/%Y at %H:%M\n"))
    f.write('http://twitter.com/'+status.author.screen_name+'/status/'+str(status.id)+'\n')
    f.write('- - - - -\n\n')

f.close()

print "Done!"
