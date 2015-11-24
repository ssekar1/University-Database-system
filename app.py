#!/usr/bin/python

import app_lib, csv, json
from bottle import route, run, request, static_file, get, post, template

pk_var = {'instructor': 'i_id', 'course' : 'c_id', 'textbook' : 't_id', 'teaches':'i_id', 'additional' : 'a_id'}

form_fields = {'course' : ['c_n', 'c_h', 'c_p'], 'instructor' : ['i_n', 'i_s'], 'textbook' : ['t_t', 't_n', 't_c'], 'teaches' : ['tc_id'], 'additional' : ['a_isbn']}

columns = {'course' : ['course_name','credit_hours', 'primary_book'], 'instructor' : ['instructor_name', 'salary'], 'textbook' : ['title', 'author', 'cost'], 'teaches' : ['instructor_id'], 'additional' : ['isbn']} 

primary_keys = {'course' : 'course_id','instructor' : 'instructor_id', 'textbook' : 'isbn', 'teaches' : 'course_id' , 'additional' : 'course_id'}

def check_type(string):
	try:
		float(string)
		return True
	except ValueError:
		try:
			int(string)
			return True
		except ValueError:
			return False

@route('/')
def home():
	return static_file("home.html", root="./web")

@post('/csv')
def mass_upload():
	inputs = ['instructor', 'course', 'textbook', 'teaches', 'additional']
	return_string = 'success'
	for item in inputs:
		temp = request.forms.get(item)
		if temp == '':
			continue
		try:
			app_lib.bulk_load(item, temp)
		except Exception as e:
			return_string = e
			
	return template('./web/csv_result.html', data=[return_string])


@post("/update")
def update():
	u_type = request.forms.get('type')
	
	temp = request.forms.get(pk_var[u_type])
	if temp == '':
		return template('.web/csv_result.html', data=["no primary key, no update"])
	pk = str(temp)

	string = ""
	for i in range(0, len(form_fields[u_type])):
		temp = request.forms.get(form_fields[u_type][i])
		if temp != '':
			string += columns[u_type][i] + ' = '
			t = str(temp)
		
			if type(temp) == str:
				t = "'" + temp + "'"
			string += t + " "
	
	return_string = 'success'
	try:
		app_lib.update(u_type, string , primary_keys[u_type], pk)
	except Exception as e:
		return_string = e
	return template('./web/csv_result.html', data=[return_string])

@post('/insert')
def insert():
	u_type = request.forms.get('type')
	
	temp = [request.forms.get(pk_var[u_type])]
	if temp[0] == '':
		return template('.web/csv_result.html', data=["no primary key, no insert"])
	pk = str(temp)

	for i in range(0, len(form_fields[u_type])):
		if type(i) == str:
			temp.append("'" + str(request.forms.get(form_fields[u_type][i])) + "'")
		else:
			temp.append(request.forms.get(form_fields[u_type][i]))

	return_string = 'success'
	
	try:
		app_lib.insert(temp, u_type)
	except Exception as e:
		return_string = e
	return template('./web/csv_result.html', data=[return_string])

@post("/delete_table")
def del_all():
	return_string = "success"
	try:
		app_lib.delete_table()
	except Exception as e:
		return_string = e
	return template('./web/csv_result.html', data=[return_string])
	

@post('/delete')
def delete():
	u_type = request.forms.get('type')
	pk_var1 = {'instructor': ['i_id'], 'course' : ['c_id'], 'textbook' : ['t_id'], 'teaches':['i_id', 'c_id'], 'additional' : ['a_id', 'a_isbn']}
	
	primary_keys1 = {'course' : ['course_id'],'instructor' : ['instructor_id'], 'textbook' : ['isbn'], 'teaches' : ['course_id', 'instructor_id'] , 'additional' : ['course_id', 'isbn']}
	
	fields = []
	command = ""	
	if u_type != "additional" and u_type != "teaches":
		command = "delete from " + u_type + " where " + \
		primary_keys1[u_type][0] + " = " + request.forms.get(pk_var1[u_type][0]) + ";"
		fields.append(request.forms.get(pk_var1[u_type][0]))
	else:
		print u_type
		print pk_var1[u_type][0]
		print pk_var1[u_type]
		command = "delete from " + u_type + " where " + \
		primary_keys1[u_type][0] + " = " + \
		 request.forms.get(pk_var1[u_type][0]) + \
		" and " + primary_keys1[u_type][1] + " = " + \
		request.forms.get(pk_var1[u_type][1]) + ";" 
		fields.append(request.forms.get(pk_var1[u_type][0]))
		fields.append(request.forms.get(pk_var1[u_type][1]))
	return_string = 'success'
	print command
	try:
		app_lib.delete_t(command)
		app_lib.constraint(u_type, fields) 
	except Exception as e:
		return_string = e

	return template('./web/csv_result.html', data=[return_string])

@post('/select')
def select():
	u_type = request.forms.get('type')
	
	fields = form_fields[u_type][:]
	fields.insert(0, pk_var[u_type])

	cols = columns[u_type][:]
	cols.insert(0, primary_keys[u_type])
	string = ''
	for i in range(0, len(fields)):
		temp = request.forms.get(fields[i])
		if temp != '':
			if check_type(temp) == False:
				string += cols[i] + " = '" + temp + "'and "
			else:
				string += cols[i] + ' = ' + str(temp) + 'and '

	string = string[:-4]

	return_string = 'no_call'
	try:
		data = app_lib.select(string, u_type)
		return_list = []
		for item in data:
			return_string = ''
			for entry in item:
				return_string += str(entry) + ' '
			return_list.append(return_string)
	except Exception as e:
		return_string = e
	return template('./web/select_result.html', data=[return_list])

run(host='localhost', port=8080, debug=True)

app_lib.close()

