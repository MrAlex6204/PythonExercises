#Require install
# $> sudo apt-get install python-mysql.connector

import mysql.connector


def display_columns(*columns):
    print "{:<11} {:<25} {:<25}".format(*columns)

def display(*row):
    print "{:<11} {:<25} {:<25}".format(*row)

qry = "Select * From TblAddresses_View"

#Create a connection object
cnn = mysql.connector.Connect(host="bookstorage.online",user="admin",password="lealtad6204....",database="dbTest")

cr = cnn.cursor()

#Execute row
cr.execute(qry)

#Display table result columns
display_columns(*cr.column_names)

#Display each row
for r in cr:
    display(*r)

#Dislpay how many results return the query
print "\n %d Row(s) found"%(cr.rowcount)
cr.close()
cnn.close()