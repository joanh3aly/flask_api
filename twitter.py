#!/usr/bin/python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import sys
import json
import dateutil.parser
from pytz import timezone
import pytz
import numpy as np
import threading
import time
import mysql.connector
import itertools
import dbconfig as cfg
from db_connect import db as cnx


class StdOutListener(StreamListener):

  def __init__(self, terms, id):
    self.sgtz = timezone('Europe/Dublin')
    self.utc = pytz.timezone('UTC')
    # Compile a regular expression pattern into a regular expression object, which can be used for matching using its match() and search() methods          
    # re.compile(pattern, flags=0)  
    self.regex = re.compile('|'.join(terms).lower())   
    self.linenum_re = re.compile(r'([A-Z][A-Z]\d+)')
    self.retweets_re = re.compile(r'^RT\s')
    self.terms = terms
    self.id = id

  def on_data(self, data):
    tweet = json.loads(data) 

    user = tweet['user']['name']
    text = tweet['text']
    # ignore text that doesn't contain one of the keywords
    matches = re.search(self.regex, tweet['text'].lower()) 	
    if not matches:
        return True

    # ignore retweets
    if re.search(self.retweets_re, tweet['text']): 
        return True

    location = tweet['user']['location']
    source = tweet['source']
    d = dateutil.parser.parse(tweet['created_at'])

    # localize time - you need to use the normalize() method to handle daylight saving time and other timezone transitions
    d_tz = self.utc.normalize(d)  
    #  building a localized time by converting an existing localized time using the standard astimezone() method
    localtime = d.astimezone(self.sgtz) 
    # time.strftime(format[, t]) - Convert a tuple or struct_time representing a time as returned by gmtime() or localtime() to a string as specified by the format argument. returns a locale dependent byte string.
    tmstr = localtime.strftime("%Y%m%d-%H:%M:%S")  
    splittedString = tmstr.split('-')[1]
    hour = splittedString.split(':')[0]

    # Find geolocation of tweeter
    geo = tweet['geo']  
  
    # is this a geocoded tweet?
    if geo and geo['type'] == 'Point':  
      coords = geo['coordinates']
    
    # print summary of tweet
    print('%s\n%s\n%s\n%s\n%s\n\n ----------------\n' % (user, location, source, tmstr, text))

    tweets = {
      'title': self.terms[0],
      'author': self.terms[1],
      'bookid': self.id,
      'dateposted': tmstr,
      'tweetcontent': text
    }  
    print('tweets ', tweets)
    cursor = cnx.cursor()
    sql = "insert into Tweets (Author,Title,DatePosted,bookid,TweetContent) values (%s, %s, %s, %s, %s)"
    values = (tweets['author'],tweets['title'],tweets['dateposted'], tweets['bookid'], tweets['tweetcontent'])
    cursor.execute(sql, values)
    # print('last ', cursor.lastrowid)
    # result = cursor.lastrowid
    cursor.close()
    cnx.commit() 
  
    return True
      
  
  def on_error(self, status):
    print('status: %s' % status)

 
