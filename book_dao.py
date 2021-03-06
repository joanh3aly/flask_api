import mysql.connector
import itertools
import dbconfig as cfg
from db_connect import db as db



class BookDao:
   
  def __init__(self):
    self.db = db

  def get_all(self):
    cursor = self.db.cursor(dictionary=True)
    sql = "SELECT * FROM Books"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result


  def find_by_id(self, id):
    cursor = self.db.cursor()
    print(id)
    sql = "SELECT * from Books WHERE ID = %s"
    print('sql ', sql)
    values = (id,)
    cursor.execute(sql, values)
    result = cursor.fetchone()
    print('result ', result)
    return result

  def create(self, book):
    cursor = self.db.cursor()
    sql = "insert into Books (Author,Title,DatePosted) values (%s, %s, %s)"
    values = (book['author'],book['title'],book['dateposted'])
    cursor.execute(sql, values)
    result = cursor.lastrowid
    cursor.close()
    self.db.commit() 
    return result


  def update(self, values):
    cursor = self.db.cursor()
    sql = "update Books set Title=%s, Author = %s, DatePosted=%s where ID = %s"
    cursor.execute(sql, values)
    result = id
    cursor.close()
    self.db.commit()
    return result

  def delete(self, id):
    cursor = self.db.cursor()
    sql = "DELETE FROM Books WHERE ID = %s"
    values = (id,)
    cursor.execute(sql, values)
    cursor.close()
    return id

  def get_tweets(self, id):
    cursor = self.db.cursor(buffered=True, dictionary=True)
    sql = "SELECT * from Tweets WHERE bookid = %s"
    values = (id,)
    cursor.execute(sql, values)
    result = cursor.fetchall()
    return result

  def get_tweets2(self):
    cursor = self.db.cursor(dictionary=True)
    sql = "SELECT * from Tweets"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# books_dao = BookDao()
