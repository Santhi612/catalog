from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship #file to file connection and total file data main file ki ravataniki

Base=declarative_base() #it design database to base

class Register(Base):
	__tablename__='register' #to create table

	id=Column(Integer,primary_key=True)
	name=Column(String(100))
	surname=Column(String(100))
	mobile=Column(String(20))
	email=Column(String(50))
	branch=Column(String(10))
	role=Column(String(40))

engine=create_engine('sqlite:///iii.db')#fields create avvataniki oka format,sqlite:///iii.db is a database name
Base.metadata.create_all(engine)#to add all fields as metadata
print("Database is created..")

class User(Base):
	__tablename__='user'
    name=Column(String(100))
	email=Column(String(50))
	password=Column(String(10))

engine=create_engine('sqlite:///use.db')#fields create avvataniki oka format,sqlite:///iii.db is a database name
Base.metadata.create_all(engine)#to add all fields as metadata
print("Database is created..")
