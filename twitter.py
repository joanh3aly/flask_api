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
    # re.compile(pattern, flags=0)  Compile a regular expression pattern into a regular expression object, which can be used for matching using its match() and search() methods
    self.regex = re.compile('|'.join(terms).lower())   
    self.linenum_re = re.compile(r'([A-Z][A-Z]\d+)')
    self.retweets_re = re.compile(r'^RT\s')
    self.terms = terms
    self.id = id

    print('imported db', cnx)
    

  # CREATE TABLE Tweets (
  #   ID int autoincrement primary key,
  #   Author varchar(255),
  #   Title varchar(255),
  #   DatePosted varchar(255),
  #   TweetContent varchar(255)
  # );

  def on_data(self, data):
    tweet = json.loads(data) #.decode('utf-8') # Deserialize (a str or unicode instance containing a JSON document) to a Python object 
    # user = tweet['user']
    # if 'user' not in tweet.keys():   # key -- This is the Key to be searched in the dictionary.
    # # if 'user' not in tweet['to']:
    #     print('No user data - ignoring tweet.')
    #     return True

    user = tweet['user']['name']
    text = tweet['text']
    # ignore text that doesn't contain one of the keywords
    print('self.regex ', self.regex)
    matches = re.search(self.regex, tweet['text'].lower()) 	
    if not matches:
        return True

    # ignore retweets
    if re.search(self.retweets_re, tweet['text']): # re_retweets from line 116 above - re.compile searches for RTs and this filters them out
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
    print("localtime %s." % localtime)
    splittedString = tmstr.split('-')[1]
    hour = splittedString.split(':')[0]
    print('hour %s' % hour)

    # Find geolocation of tweeter
    geo = tweet['geo'] 
    print("geo", geo)
      
  
    # is this a geocoded tweet?
    if geo and geo['type'] == 'Point':  
      coords = geo['coordinates']
      print("coords", coords)
    
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

 
