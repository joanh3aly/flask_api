from flask import Flask, jsonify, render_template, request, abort
import time
from book_dao import BookDao 
from twitter import *
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()
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
from twitter import StdOutListener

def create_app():
    app = Flask(__name__)
    csrf.init_app(app)

app = Flask(__name__)
books_class = BookDao()

@app.route("/")
def main():
    return render_template('main.html', reload = time.time())

@app.route("/api/books")
def api_books():
    results = books_class.get_all()
    results_lower = []
    for each in results:
        results_lower.append({k.lower(): v for k, v in each.items()}) 
    # print('results_lower ', results_lower)
    return jsonify(results_lower)

# curl -i -H "Content-Type:application/json" -X POST -d '{"title":"Sherlock Holmes", "author":"AC Doyle","date_posted":"1/12/2019"}' http://127.0.0.1:5000/api/books
@app.route('/api/books', methods=['POST'])
@csrf.exempt
def create():
    print('req', request)
    if not request.json:
      abort(400)
    # other checking
    books = {
      'title': request.json['title'],
      'author': request.json['author'],
      'dateposted': request.json['dateposted']
    }  
    print('req', books['title'])
    results = books_class.create(books)
    print('results', results)
    return jsonify(results)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Title\":\"hello\",\"Author\":\"someone\",\"Price\":123}" http://127.0.0.1:5000/books/1
@app.route('/api/books/<int:id>', methods=['PUT'])
def update(id):
    foundBook = books_class.find_by_id(id)
    print('foundBook ', foundBook)
    if not foundBook:
        abort(404)
    if not request.json:
        abort(400)
    reqJson = request.json
    print('foundBook ', type(foundBook))
    print('foundBook ', foundBook)

    if 'title' in reqJson:
        title = reqJson['title']
    if 'author' in reqJson:
        author = reqJson['author']
    if 'dateposted' in reqJson:
        dateposted = reqJson['dateposted']
    values = (title, author, dateposted, id)
    books_class.update(values)
    return jsonify(id)

@app.route('/api/books/<int:id>' , methods=['DELETE'])
def delete(id):
  books_class.delete(id)
  return jsonify({"done":True})

@app.route('/api/tweets/<int:id>', methods=['GET'])
def tweets(id):
    foundBook = books_class.find_by_id(id)
    print('foundBook app', foundBook)
    print('foundBook ', type(foundBook))
    print('book id ', foundBook[0])
    if not foundBook:
        abort(404)

    TERMS = [foundBook[1], foundBook[2]]
    listener = StdOutListener(TERMS, foundBook[0])
    # The consumer keys can be found on your application's Details page located at https://dev.twitter.com/apps (under "OAuth settings")
    CONSUMER_KEY="hVXOnpdbN0uLtAUSEjOdUgL6b"
    CONSUMER_SECRET="CWYDtRZTFJdN5WQO6WaVkNoLYDuWpBFilAhFZEnbqqQKMfDX8f"
    ACCESS_TOKEN="1577934554-zSVtsvcwYW9t6ZWom8iBtlcim4R7YFoEvs4uoXy"
    ACCESS_TOKEN_SECRET="6mX3Sf76QZurtpKzZHsiTE21n3V7RI1NkjdUntfKQwGxr"

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener, timeout=60)  
    print("Listening to filter stream...")
    print("stream object")
    print(stream)
    print('stream type ', stream)
    stream.filter(track=TERMS) 
    
    return jsonify(id)

@app.route('/api/view_tweets/<int:id>', methods=['GET'])
def get_all_tweets(id):
    print('id ', id)
    results = books_class.get_tweets(id)
    print('results ', type(results))
    results_lower = []
    for each in results:
        results_lower.append({k.lower(): v for k, v in each.items()})     
    return jsonify(results_lower)

@app.route('/api/view_tweets/', methods=['GET'])
def get_all_tweets2():
    results = books_class.get_tweets2()
    print('results ', type(results))
    results_lower = []
    for each in results:
        results_lower.append({k.lower(): v for k, v in each.items()})  
    return jsonify(results_lower)

@app.route('/api/count_tweets/<int:id>', methods=['GET'])
def count_tweets(id):
    print('id ', id)
    results = books_class.get_tweets(id)
    print('count results ', results)
    results_len = len(results)
    print('count results ', results_len)
    return jsonify(results_len)


if __name__ == "__main__":
  app.run(debug='True')