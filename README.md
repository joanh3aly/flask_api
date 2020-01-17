# Flask API

This is a CRUD app using the Flask python framework that can create, display and delete book entries. AJAX is used to interface between the HTML/JavaScript and the server side Python that accesses the SQL database.

A file called twitter.py uses a package called Tweepy to stream tweets live from Twitter using the Twitter API. This required Oauth authentication.
There is a button called 'find tweets' for each book listed which triggers the Tweepy library to stream tweets that have the the book's title and/or author in the content of the tweet. These tweets are then saved in the 'Tweets' table. 
A button called 'view tweets' displays a list of collected tweets related to a specific book.
