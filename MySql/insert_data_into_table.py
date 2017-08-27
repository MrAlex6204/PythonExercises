#Require install
# $> sudo apt-get install python-mysql.connector

import mysql.connector
import requests
import json
import config

def display(**row):    
    #Display print row data in screen
    print "{FirstName:25} {LastName:25} {Email:15}".format(**row)


#Get data from api service as json array object
data_source_url = "http://beta.json-generator.com/api/json/get/V1WiBrCRg"

#Do a requets to the api service and get content
req = requests.get(data_source_url)

#Parse json array content request to an Python Dictonary array
records  = json.loads(req.content)

#Query template
qry = """
        Insert Into TblEmployee (FirstName,LastName,Email,HireDate) 
        Values (%(FirstName)s,%(LastName)s,%(Email)s,Now());
       """

#Create a connection object parsing  auth Dictonary as kwargs
cnn = mysql.connector.Connect(**config.auth)

#Create cursor as named tuple 
cr = cnn.cursor()

counter = 0

print "Storing data in Remote server : %(host)s | Database : %(database)s \n"%(config.auth)
for r in records:
    try:
        #Execute the query template and pass through the row dictonary
        display(**r)
        cr.execute(qry,r)
        counter+=1    
    except Exception as e:        
        print e

cnn.commit()
print "\n\n%d Row(s) Inserted "%(counter)
