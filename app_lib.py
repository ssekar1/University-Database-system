#!/usr/bin/python3.4

import sqlite3, csv

conn = sqlite3.connect('project.db')
cur = conn.cursor()

#conn.isolation_level="EXCLUSIVE" #now have to commit transactions
conn.isolation_level=None #now autocommit. (default)

#returns list of primary keys for table
def get_pk(table):
	cur.execute("pragma table_info(" + table + ")")
	primary_key = cur.fetchall()

	return [x[1] for x in [list(y) for y in primary_key] if x[-1] == 1] #may be dealing with composite keys

#returns 1 for good, 0 for bad
#it is bad if there is a course id in course which is not in teaches
def check_teaches():
	cur.execute("select course_id from course where course_id not in (select course_id as id from teaches);")
	if cur.fetchall() == []: #fetchall returns a list of tuples
		return 1
	return 0

#returns 1 for good, 0 for bad
#it is bad if there is a course id in course which is not in has
def check_has():
	cur.execute("select course_id from course where course_id not in (select course_id as id from has);")
	if cur.fetchall() == []:
		return 1
	return 0

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
def delete(values, table):
	pk = get_pk(table)
	[cur.execute("delete from " + table + " where " + str(pk[0]) + "=" + str(x) + ';') for x in values]

#assumes all parameters are not lists
def update(table, string, pk, pk_val):
	cur.execute("update " + table + " set " + string + " where " + pk + " = " + pk_val + ";")

#takes a table and a csv file. puts data in
def bulk_load(table, csv_file):
	with open(csv_file, "r") as x:
		x.readline() #removes the first item in x
		reader = csv.reader(x, delimiter=',')
		[insert(y, table) for y in reader]

def close():
	conn.close()

'''
bulk_load("textbook", "book.csv")
cur.execute("select * from textbook;")
print(cur.fetchall())

insert([1, 'a', 1], "course")
cur.execute("select * from course;")
print(cur.fetchall())
update("course", "course_name", "b", 1)
cur.execute("select * from course;")
print(cur.fetchall())
delete([1], "course")
cur.execute("select * from course;")
print(cur.fetchall())
'''
#cur.execute("select * from course;")
#print(cur.fetchall())
#cur.execute('select * from course;')
#print(cur.fetchall())

#print(check_teaches(),"\n",check_has())

#conn.close()

