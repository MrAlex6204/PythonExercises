import scrapper
import json



print "Scrapping information from "
print "http://www.paginasamarillas.com.ar"

fs = open('data.json','w+')
data = scrapper.get_site_content()

print "Saving information info dat.json"

fs.write(json.dumps(data))
fs.close()

print "[DONE SUCCESSFULLY!]"
