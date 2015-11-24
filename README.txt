Dear User,

app.py is an application program to interact with a sqlite database. To use the application program, run 
./app.py and then, in your browser (preferably using chrome), go to http://localhost:8080

The database, project.db, should be in the same directory as app.py. the folder, web, should also be in the same directory as project.db. 

for mass loading of CSV files: I have assumed that the CSV files will have the column names as the first line of the file. Therefore, the first line of each csv file will be ignored.

the csv file names are:
	course.csv
	book.csv
	instructor.csv
	additional.csv
	textbook.csv

the schema and e-r diagram are in proj_analysis.docx

the script to make the tables is: make_tables 

Assumptions:
-I will assume that the 'teaches' and 'additional' relations can not be 
	updated, because they only contain primary keys
-I will assume that the primary textbook for a course should be an attribute 
	for a course.
-I assume that multiple courses may have the same primary textbook.
-I assume that the main textbook for a course should be an attribute of
	the course entity, and the there should be an additional relation for 
	other
textbooks associated with a course.
