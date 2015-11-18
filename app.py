#!/usr/bin/python3.4

import app_lib, csv, json
from bottle import route, run, request, static_file, get, post, template

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
def u_inst():
	u_type = request.forms.get('type')
	pk_var = {'instructor': 'i_id', 'course' : 'c_id', 'textbook' : 't_id', 'teaches':'ti_id', 'additional' : 'a_id'}
	temp = request.forms.get(pk_var[u_type])
	if temp == '':
		return template('.web/csv_result.html', data=["no primary key, no update"])
	pk = str(temp)

	form_fields = {'course' : ['c_n', 'c_h', 'c_p'], 'instructor' : ['i_n', 'i_s'], 'textbook' : ['t_t', 't_n', 't_c'], 'teaches' : 'tc_id', 'additional' : 'a_isbn'}

	columns = {'course' : ['course_name','credit_hours', 'primary_book'], 'instructor' : ['instructor_name', 'salary'], 'textbook' : ['title', 'author', 'cost'], 'teaches' : ['instructor_id'], 'additional' : ['isbn']} 

	primary_keys = {'course' : 'course_id','instructor' : 'instructor_id', 'textbook' : 'isbn', 'teaches' : 'course_id' , 'additional' : 'course_id'}

	string = ""
	for i in [0,1]:
		temp = request.forms.get(form_fields[u_type][i])
		if temp != '':
			string += columns[u_type][i] + ' = '
			t = str(temp);
		
			if type(temp) == str:
				t = "'" + temp + "'"
			string += t + " "
	
	return_string = 'success'
	try:
		app_lib.update(u_type, string , primary_keys[u_type], pk)
	except Exception as e:
		return_string = e
	return template('./web/csv_result.html', data=[return_string])
  
run(host='localhost', port=8080, debug=True)

app_lib.close()

