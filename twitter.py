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
from db_connect import db as db

# db = mysql.connector.connect(
#   # host="localhost",
#   # user="root",
#   # password="",
#   # database="Books",
#   # auth_plugin='mysql_native_password'
#   host = cfg.mysql['host'], 
#   user = cfg.mysql['user'], 
#   password = cfg.mysql['password'], 
#   database = cfg.mysql['database'], 
#   auth_plugin='mysql_native_password'
# )

class StdOutListener(StreamListener):

  def __init__(self, terms):
    self.sgtz = timezone('Europe/Dublin')
    self.utc = pytz.timezone('UTC')          
    self.regex = re.compile('|'.join(terms).lower())   # re.compile(pattern, flags=0)  Compile a regular expression pattern into a regular expression object, which can be used for matching using its match() and search() methods
    self.linenum_re = re.compile(r'([A-Z][A-Z]\d+)')
    self.retweets_re = re.compile(r'^RT\s')
    self.terms = terms

  # def create_tweets(self, title, author, dateposted, tweetcontent):
    # tweets = {
    #   'title': title,
    #   'author': author,
    #   'dateposted': dateposted,
    #   'tweetcontent': tweetcontent
    # }  
    # cursor = db.cursor()
  #   print('tweets. ', tweets['author'])
  #   sql = "insert into Tweets (Author,Title,DatePosted,TweetContent) values (%s, %s, %s, %s)"
  #   values = (tweets['author'],tweets['title'],tweets['dateposted'],tweets['tweetcontent'])
  #   cursor.execute(sql, values)
  #   print('last ', cursor.lastrowid)
  #   result = cursor.lastrowid
  #   cursor.close()
  #   self.db.commit() 
  #   # db.close()
  #   return result

  # CREATE TABLE Tweets (
  #   ID int autoincrement primary key,
  #   Author varchar(255),
  #   Title varchar(255),
  #   DatePosted varchar(255),
  #   TweetContent varchar(255)
  # );

  def on_data(self, data):
    tweet = json.loads(data) #.decode('utf-8') # Deserialize (a str or unicode instance containing a JSON document) to a Python object 
    # print('tweet.keys() ', tweet.keys())
    # print('tweet.keys() ', tweet.keys())
    # user = tweet['user']
    # if 'user' not in tweet.keys():   # key -- This is the Key to be searched in the dictionary.
    # # if 'user' not in tweet['to']:
    #     print('No user data - ignoring tweet.')
    #     return True

    enc = lambda x: x.encode('latin1', errors='ignore')  # lambda :	 creation of anonymous functions // .encode Encodes obj using the codec registered for encoding. The default encoding is 'ascii'.
    # user = enc(tweet['user']['name']) # enc function from .encode into latin , line 118 above
    user = tweet['user']['name']
    text = tweet['text']
    # print("encoded", str(text))
    # print("encoded type ", type(text))

    # ignore text that doesn't contain one of the keywords
    print('self.regex ', self.regex)
    matches = re.search(self.regex, tweet['text'].lower()) 	
    if not matches:
        return True

    # ignore retweets
    if re.search(self.retweets_re, tweet['text']): # re_retweets from line 116 above - re.compile searches for RTs and this filters them out
        return True

    # location = enc(tweet['user']['location'])
    location = tweet['user']['location']
    # source = enc(tweet['source'])
    source = tweet['source']
    # d = dateutil.parser.parse(enc(tweet['created_at']))
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
    if geo and geo['type'] == 'Point':   # see JSON format to see where 'POint' comes from 
      # collect location of mrt station
      coords = geo['coordinates']
      print("coords", coords)
      # print coords[1]
    
    # print summary of tweet
    print('%s\n%s\n%s\n%s\n%s\n\n ----------------\n' % (user, location, source, tmstr, text))

    tweets = {
      'title': self.terms[0],
      'author': self.terms[1],
      'dateposted': tmstr,
      'tweetcontent': text
    }  
    print('tweets ', tweets)
    # self.create_tweets( self.terms[0], self.terms[1], tmstr, text)
    cursor = db.cursor()
    sql = "insert into Tweets (Author,Title,DatePosted,TweetContent) values (%s, %s, %s, %s)"
    values = (tweets['author'],tweets['title'],tweets['dateposted'],tweets['tweetcontent'])
    cursor.execute(sql, values)
    print('last ', cursor.lastrowid)
    result = cursor.lastrowid
    cursor.close()
    db.commit() 
  
    return True
      
  
  def on_error(self, status):
    print('status: %s' % status)

 
