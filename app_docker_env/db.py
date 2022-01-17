from flask import Flask
import mysql.connector
import os


def connection_database():
	try:
		host  = os.environ['DATABASE_URL']
		user  = os.environ['DATABASE_USER']
		password = os.environ['DATABASE_PASSWORD']
		database = os.environ['DATABASE']
		conn = mysql.connector.connect(host=host,database=database,user=user,password=password)
		print(f"Connection succeeded: {conn}")
		return conn
	except Exception as e:
		print(e)
		return -1



