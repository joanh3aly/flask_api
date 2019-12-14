import dbconfig as cfg
import mysql.connector

db = mysql.connector.connect(
  host = cfg.mysql['host'], 
  user = cfg.mysql['user'], 
  password = cfg.mysql['password'], 
  database = cfg.mysql['database'], 
  # auth_plugin='mysql_native_password'
)