=============================
<p align="center" >
  <img src="https://raw.github.com/c0ding/tweetuoso/master/tweetuoso/doc/tweetuoso.banner.png" alt="Tweetuoso" title="Tweetuoso">
</p>
=============================

[![Downloads](https://pypip.in/d/tweetuoso/badge.png)](https://crate.io/packages/tweetuoso/)

## Description

**Tweetuoso** is a very light Twitter Command-line client developed in Python. The main goal of Tweetuoso is to become a fully-fledged twitter client with the same functions as the online version.

For now, it allows you to:

* check your timeline
* post tweets
* show tweets that mentionned you
* get your profile details
* follow or unfollow people
* search for 'query'
* stalk people (or yourself)
* show current trends
* automatically followback your followers
* Archive all your tweets to a text file

More is still to come...


## Console screenshot (80x24):


![screenshot](https://raw.github.com/c0ding/tweetuoso/master/tweetuoso/doc/screenshot.png)


## Installation


Pre-requisites:

* Python 2.6+ (not tested with Python 3+)
* tweepy >= 2.1 (for a Twitter API connection, obviously)
* requests 1.1.0
* colorama 0.2.5
* GitPython 0.3.2 (if you wish to use tweet_commit)
* pytz
* python-setuptools 
* Working API keys from Twitter


### From source

**Remember to configure Tweetuoso before install it!**

Get the latest version (from GitHub):

    $ wget -O /tmp/tweetuoso-last.tgz https://github.com/c0ding/tweetuoso/tarball/master
    $ sudo apt-get update
    $ sudo apt-get install python-setuptools python-tweepy python-requests
    $ cd /tmp
    $ tar zxvf tweetuoso-last.tgz
    $ chmod -R 777 c0ding-tweetuoso-*    
    $ cd c0ding-tweetuoso-*/
    $ python setup.py install


### From PyPi

    $ pip install tweetuoso

## Configuration


### Step 1: Register a new client app with Twitter


Navigate to https://dev.twitter.com/apps/new. You might have to log into the Twitter Developers site first, if you’re not already.
Fill in the registration fields as follows:

![screenshot](https://raw.github.com/c0ding/tweetuoso/master/tweetuoso/doc/registration.png)

**Note**: whatever you specify for Application Name will be the “via” name your followers see in the details of tweets issued from your command line app.


### Step 2: OAuth settings


Next, the app needs to be authorized to connect to your account so it can send tweets under your name. Paste the **Consumer Key** and **Consumer Secret** into config.py file. Then save and run **Tweetuoso** on your system.

![screenshot](https://raw.github.com/c0ding/tweetuoso/master/tweetuoso/doc/keys.png)

You should see a prompt like this:

    $ Please visit this url to get your access keys: <url>
    $ PIN:

Open that URL in your browser. You should see the standard OAuth Twitter connection screen. Click **Allow**.

Twitter will then provide you with a PIN code that authenticates the connection between the client app and your Twitter account.

Enter this PIN into the Tweetuoso prompt:

    $ PIN: 2781961

Tweetuoso will then print out another key/secret pair: (The values will be different each time!)

    $ access_token = '124242RCyi3g0cZ4r5BWL047rsh0S0yv5VxAGwTKCOsHAb'
    $ access_secret = 'kaTXiC489qo8y6haTBSlwOqR1syG83tzPG2StdQ'

Keep this information on your screen because we’ll need it in the next step.

### Step 3: Paste the keys into Tweetuoso


Paste the **Access Token** and **Access Secret** from the end of step 2 into the auth.py file, filling the **access_token** and **access_secret** constants.

### Step 4: Application Type


On the Twitter Developer website, navigate to the **Settings** tab. Allow your application Read, Write and direct messages access.

![screenshot](https://raw.github.com/c0ding/tweetuoso/master/tweetuoso/doc/access.png)

Finally, we’re all set up. Our command line app is registered as a Twitter client and the app is connected to our Twitter user account.

## Running


Simply follow the steps above, edit the config.py file to suit your needs and launch tweetuoso.py. Enjoy!


## License


```
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004
 
Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
 
Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.
 
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
 
 0. You just DO WHAT THE FUCK YOU WANT TO.


```


## Thanks to


* Sven Steinbauer ([Svenito on Github](https://github.com/Svenito))


**Feel free to report issues or to contribute**
