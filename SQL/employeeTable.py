'''  =======================================================================================================
    | This code creates an employeeTable and fills in the employee ID, employee name, and employee gender.   |
    | Later, the SQLite command is used to count the total number of employees with the different gender and |
    | sort them in descending order.                                                                         |
     =======================================================================================================
'''


#import module to connect to sqlite database
import sqlite3

#The sqlite3.connect commands connect to the data base
connecTo = sqlite3.connect('gender_table.sqlite')

#'cursor' is conceptually similar to open() when dealing with text files
cursor  = connecTo.cursor()

table_name = 'employeeTable'

#execute is to run command similar to running command in DB Browser for SQLite
cursor.execute('DROP TABLE IF EXISTS employeeTable')
cursor.execute('CREATE TABLE employeeTable (empId INTEGER, name TEXT, gender TEXT)')


#Use list comprehension and list expressions to loop in the upcoming section
empId  = [index for index in range(1,6)]
name   = ['Andrew','Raju','Priya','Joseph','Sarah']
gender = ['M','M','F','M','F']


for index,name in zip(empId,name):    
    cursor.execute('INSERT INTO employeeTable (empId,name,gender) VALUES (?,?,?)',(index,name,gender[index-1]))


#Select all content that is in the gender table
cursor.execute('SELECT * FROM employeeTable')

print()
print('All rows and columns of employeeTable')
print()
for row in cursor:
    print(row)


#Count how many male and female are in the table,
#Select only the gender and cout(gender) columns,
#Goup it according to gender and Order it in the descending order
cursor.execute('SELECT gender,count(gender) AS no_of_male_female \
                FROM employeeTable \
                GROUP BY gender  \
                ORDER BY no_of_male_female DESC;')

print()
print('Show total number of male and female in the employeeTable')
print()
for row in cursor:
    print(row)


#IF I want to add a new column, then I have to alter the existing table

cursor.execute('ALTER TABLE employeeTable\
                ADD Department TEXT')


Department = ['ComputerScience','Chemistry','Physics','Math','Geology']

for index,item in enumerate(Department):
    cursor.execute('UPDATE employeeTable SET Department=? WHERE empId=?',(item,index+1))


cursor.execute('SELECT * FROM employeeTable')
#cursor.execute('SELECT * FROM employeeTable \
                #WHERE name LIKE An% AND Pr%')
print()
print('Now the table has been altered, a new column is added with employee department')
print()
for row in cursor:
    print(row)

print()
print('Find the name of employee who work in the Physics and math Department')
print()

cursor.execute('SELECT name, Department \
                FROM employeeTable \
                WHERE Department IN ("Physics","Math");')

for row in cursor:
    print(row)

connecTo.close()
