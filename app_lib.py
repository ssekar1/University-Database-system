#!/usr/bin/python

import sqlite3, csv

conn = sqlite3.connect('project.db')
cur = conn.cursor()

#conn.isolation_level="EXCLUSIVE" #now have to commit transactions
conn.isolation_level=None #now autocommit. (default)


def test_constraint():
	return "success"

def delete_table():
	l = ['instructor', 'course' , 'textbook', 'teaches', 'additional']
	for i in l:
		cur.execute("delete from " + i + " where 1=1;")

def delete_t(command):
	cur.execute(command)

def constraint(table, fields):
	if table == "instructor":
		cur.execute("delete from course where course_id in (select course_id from teaches where instructor_id = " + fields[0] + ");")
		cur.execute("delete from teaches where instructor_id = " \
			+ fields[0] + ";")
		cur.execute("delete from additional where course_id not in (select course_id from course);")

	if table == "teaches":
		cur.execute("delete from course where course_id = " + fields[0] + ";")
		cur.execute("delete from instructor where instructor_id = " + fields[1] + ";")
		cur.execute("delete from additional where course_id not in (select course_id from course);")

	if table == "textbook":
		cur.execute("delete from teaches where course_id in (select course_id from course where primary_book = " + fields[0] + ");")
		cur.execute("delete from additional where isbn = " + fields[0] + ";")
		cur.execute("delete from course where primary_book = " + fields[0] + ";")

#you had better check that the list, values, has the same number of columns as table does
def insert(values, table):
	query = "insert into " + table + " values(?"
	for item in values[:-1]:
		query += ",?"
	query += ")"

	cur.execute(query, values)
		
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
	cur.execute("select * from  " + table + " where " + string + ";")
	foo = list(cur.fetchall())
	ret = []
	for item in foo:
		ret.append(list(item))
	return ret

def close():
	conn.close()




