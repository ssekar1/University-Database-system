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

run(host='localhost', port=8080, debug=True)

app_lib.close()

