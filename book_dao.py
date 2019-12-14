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
    desc = cursor.description
    column_names = [col[0] for col in desc]
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
    print('book. ', book['author'])
    sql = "insert into Books (Author,Title,DatePosted) values (%s, %s, %s)"
    values = (book['author'],book['title'],book['dateposted'])
    cursor.execute(sql, values)
    print('last ', cursor.lastrowid)
    result = cursor.lastrowid
    cursor.close()
    self.db.commit() 
    return result


  def update(self, values):
    cursor = self.db.cursor()
    print('values ', values)
    # print('book. ', book['author'])
    sql = "update Books set Author = %s, Title=%s, DatePosted=%s where ID = %s"
    # values = (book['author'],book['title'],book['date_posted'],id)
    cursor.execute(sql, values)
    # print('last ', cursor.lastrowid)
    result = id
    cursor.close()
    self.db.commit()
    return result

  def delete(self, id):
    cursor = self.db.cursor()
    print('id is ', id)
    sql = "DELETE FROM Books WHERE ID = %s"
    values = (id,)
    cursor.execute(sql, values)
    cursor.close()
    # self.db.commit() 
    return id

  def get_tweets(self, id):
    cursor = self.db.cursor(dictionary=True)
    sql = "SELECT * from Tweets WHERE bookid = %s"
    print('sql ', sql)
    values = (id,)
    cursor.execute(sql, values)
    result = cursor.fetchall()
    print('result ', result)
    return result

books_dao = BookDao()

# student_dao.create(('foo', 'bar'))


# result = student_dao.get_all()
# for x in result:
#   print(x)