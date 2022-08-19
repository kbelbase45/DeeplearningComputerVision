import sqlite3
import pandas as pd


Description = '''
                 --------------------------------------------------------------------------------------------
                | This script will first delete if there is a table named email_count in the database and   |
                | then creates a table with the same name email_count containing email and count Columns.   |
                | The script look for the emails in the file 'mbox-short.txt' or in other given name then   |
                | counts their occurances. However, the only caveat is that the email should look something |
                | like this: "From: something@random". If not, the code on line 40 needs to be changed.     |
                | The script combines the Python and the SQL command. For SQL, SELECT, INSERT, and UPDATE   |
                | are used. Text files containing emails are in Data folder                                 |
                ---------------------------------------------------------------------------------------------
              '''

print(Description)

#This creates file name emaildb.sqlite
conn = sqlite3.connect('emaildb.sqlite')
cur  = conn.cursor()

#Delete table Counts if it already exits
cur.execute('DROP TABLE IF EXISTS email_count')


#Create table with name Counts that has two field email as text and counts as integer
cur.execute('''
    CREATE TABLE email_count (email TEXT,count INTEGER)
    ''')

#Ask user to give the file name 
fname = input('Enter file name:   ')
print(' ')
#If len(fname)<1 means user do not provide file name
if (len(fname)<1): fname = 'mbox-short.txt'
fh = open(fname)

for line in fh:
    #Check if string in line starts with From
    if not line.startswith('From: '):continue
    
    #Split content of line according to presence of space
    pieces = line.split()
    email  = pieces[1]
    
    #The  ? in the following is the data filling technique
    cur.execute('SELECT count FROM email_count WHERE email= ? ',(email,))
    
    row  = cur.fetchone()
    if row is None:
        #If nothing in the row that happens for the first time when it encounters email.
        cur.execute('INSERT INTO email_count (email,count) VALUES (?,1)',(email,))
    else:
        #In the next step
        cur.execute('UPDATE email_count SET count = count + 1 WHERE email = ?',(email,))
    
    #The database keeps the information in memory and at some point it has to be written to disk.
    #So here this commit enforce to write every time in disk. This can be updated in suh a way that
    #just to write just after 10 item or 100 item.
    conn.commit()
    
sqlstr = 'SELECT email, count FROM email_count ORDER BY count DESC LIMIT 10'

email_add = list()
count_no  = list()

for row in cur.execute(sqlstr):    
    email_add.append(str(row[0]))
    count_no.append(row[1])
    print(str(row[0]), row[1])

#Close the sql connection
print()
print(f'Data is saved in emaildb.sqlite, open it with sqlbrowser not by text editor. ')
cur.close()


#Create readable data frame with email and its occurances
data_table = pd.DataFrame({'Email_ID':email_add, \
                           'Total_Count':count_no},columns=['Email_ID','Total_Count'])

#Save the dataframe as scv format
data_table.to_csv('Email_Count.dat',index=False)



