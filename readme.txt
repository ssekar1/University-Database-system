Dear User,

The ER diagram,  table schemas, and sql scripts to create the tables are located in the proj_analysis.docx.

app.py is an application program to interact with a sqlite database. To use the application program, run 
./app.py and then, in your browser (preferably using chrome), go to http://localhost:8080

The database, proj.db, should be in the same directory as app.py. the folder, web, should also be in the same directory as proj.db. 

for mass loading of CSV files: I have assumed that the CSV files will have the column names as the first line of the file. Therefore, the first line of each csv file will be ignored.



Assumptions:
I will assume that the 'teaches' and 'additional' relations can not be updated, because they only contain
primary keys

i will assume that the primary textbook for a course should be an attribute for a course.
