#Require install
# $> sudo apt-get install python-mysql.connector

import mysql.connector
import requests
import json
import config

def display_employee(**row):    
    #Display print row data in screen
    print "{FirstName:25} {LastName:25} {Email:15}".format(**row)


def display_address(**row):
    print "{Employee_Id:2} {Address:25}".format(**row)

def display_sales(**row):
    print "{Employee_Id:2} {Amount:25} {Comment:25}".format(**row)

#Get data from api service as json array object
employee_data_source_url = "http://next.json-generator.com/api/json/get/V1WiBrCRg"
address_data_source_url = "http://next.json-generator.com/api/json/get/4kMLXjpdX"
sales_data_source_url = "http://next.json-generator.com/api/json/get/MLv346R"

#Do a requets to the api service and get content
employee_req = requests.get(employee_data_source_url)
address_req = requests.get(address_data_source_url)
sales_req = requests.get(sales_data_source_url)
#Parse json array content request to an Python Dictonary array
employee_records  = json.loads(employee_req.content)
address_records = json.loads(address_req.content)
sales_records = json.loads(sales_req.content)
#Query template
insert_qry = """
        Insert Into TblEmployee (FirstName,LastName,Email,HireDate) 
        Values (%(FirstName)s,%(LastName)s,%(Email)s,Now());
       """
insert_address = """
        Insert Into TblAddress(Employee_Id,Address)
        Values(%(Employee_Id)s,%(Address)s)
        """
insert_sales = """
        Insert Into TblSales(Employee_Id,Comment,Amount,SaleDate)
        Values(%(Employee_Id)s,%(Comment)s,%(Amount)s,Now())
        """
#Create a connection object parsing  auth Dictonary as kwargs
cnn = mysql.connector.Connect(**config.auth)

#Create cursor as named tuple 
cr = cnn.cursor()

counter = 0

print "Storing data in Remote server : %(host)s | Database : %(database)s \n"%(config.auth)
for r in employee_records:
    try:
        #Execute the query template and pass through the row dictonary
        display_employee(**r)
        cr.execute(insert_qry,r)
        counter+=1            
    except Exception as e:        
        print e

cnn.commit()

counter = 201
for r in address_records:
    try:
        r['Employee_Id'] = counter
        display_address(**r)
        cr.execute(insert_address,r)
        counter+=1
    except Exception as e:
        print e
cnn.commit()

counter = 201
for r in sales_records:
    try:
        r['Employee_Id'] = counter
        display_sales(**r)
        cr.execute(insert_sales,r)
        counter+=1
    except Exception as e:
        print e
cnn.commit()


print "\n\n%d Row(s) Inserted "%(counter)
