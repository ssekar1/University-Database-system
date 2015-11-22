#!/usr/bin/python

import sqlite3, csv

conn = sqlite3.connect('project.db')
cur = conn.cursor()

conn.isolation_level="EXCLUSIVE" #now have to commit transactions
#conn.isolation_level=None #now autocommit. (default)

#returns 1 for good, 0 for bad
#it is bad if a consistency contrtaint is violated
def fail():
	cur.execute("select course_id from teaches where course_id not in (select course_id as id from course);")
	if cur.fetchall() != []: #fetchall returns a list of tuples
		return "course_id in teaches but not in course"

	cur.execute("select instructor_id from teaches where instructor_id not in (select instructor_id as id from instructor);")
	if cur.fetchall() != []: #fetchall returns a list of tuples
		return "instructor_id in teaches but not in instructor"

	cur.execute("select primary_book from course where primary_book not in (select isbn from textbook);")
	if cur.fetchall() != []: #fetchall returns a list of tuples
		return "primary_book in course but not in textbook"

	cur.execute("select course_id from additional where course_id not in (select course_id as id from course);")
	if cur.fetchall() != []: #fetchall returns a list of tuples
		return "course_id in additional but not in course"

	cur.execute("select isbn from additional where isbn not in (select isbn as id from textbook);")
	if cur.fetchall() != []: #fetchall returns a list of tuples
		return "isbn in additional but not in textbook"

	return "success"

def test_constraint():
	string = fail()
	if string != "success":
		conn.rollback() 
	else:
		conn.commit()
	return string

def delete():
	cur.execute("delete from additional where course_id not in (select course_id as c_id from course) or isbn not in (select isbn as id from textbook);")
	cur.execute("delete from course where primary_book not in (select isbn from textbook);")
	cur.execute("delete from teaches where course_id not in (select course_id as c_id from course) or instructor_id not in (select instructor_id as id from instructor);")
	conn.commit()
#you had better check that the list, values, has the same number of columns as table does
def insert(values, table):
	query = "insert into " + table + " values(?"
	for item in values[:-1]:
		query += ",?"
	query += ")"
	cur.execute(query, values)
		
#values is a list
#the table had better have a primary key
#better verify that the values aren't sql injections
def delete(string, table):
	cur.execute("delete from " + table + " where " + string)
	delete()

#assumes all parameters are not lists
def update(table, string, pk, pk_val):
	cur.execute("update " + table + " set " + string + " where " + pk + " = " + pk_val + ";")

#takes a table and a csv file. puts data in
def bulk_load(table, csv_file):
	with open(csv_file, "r") as x:
		x.readline() #removes the first item in x
		reader = csv.reader(x, delimiter=',')
		[insert(y, table) for y in reader]

#selects tuples matching constraint, returns a list
def select(string, table):
	if("*" in string): # checks if * is in the sent string, could not get it to work for specific fields
		cur.execute("select * from "+ table+ ";")
	else:
		cur.execute("select * from  " + table + " where " + string + ";")
	foo = list(cur.fetchall())
	ret = []
	for item in foo:
		ret.append(list(item))
	return ret

def close():
	conn.close()



