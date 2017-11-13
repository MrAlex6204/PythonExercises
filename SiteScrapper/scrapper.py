import re
import requests
from bs4 import BeautifulSoup

#Sections names available to scrapp 
#"restaurantes","hoteles","farmacias","abogados","inmobiliarias","repuestos-para-el-auto"
lst_sections = {"repuestos-para-el-auto"}
parent_url = 'http://www.paginasamarillas.com.ar/b/%s/_ordAZ/p-%s'

def trim(t):
    return "".join([c for c in t if not c in '\n\t\r']) if t else ""

def get_section_content(section,page_no):
    url  = parent_url%(section,page_no)
    req  = requests.get(url)
    if not req.status_code == 404:
        return BeautifulSoup(req.content,"html.parser")
    else:
        None

def fetch_data(html_element,section_name):
    data = {
            "name":trim(html_element.find("div",attrs={"class":"t1 business-name"}).text) if html_element.find("div",attrs={"class":"t1 business-name"}) else "",
            "address": trim(html_element.find("span",attrs={"itemprop":"streetAddress"}).text) if html_element.find("span",attrs={"itemprop":"streetAddress"}) else "",
            "location": trim(html_element.find("span",attrs={"itemprop":"addressLocality"}).text) if html_element.find("span",attrs={"itemprop":"addressLocality"}) else "",
            "url": trim(html_element.find("a",attrs={"class":"t2 business-web"}).text) if html_element.find("a",attrs={"class":"t2 business-web"}) else "",
            "tags":trim((html_element.find("div",attrs={"class":"t2 line line-hideable-maximap"}).text if html_element.find("div",attrs={"class":"t2 line line-hideable-maximap"}) else "")),
            "phone" :trim(html_element.find("a",attrs={"id":"VerTelefono"}).text if html_element.find("a",attrs={"id":"VerTelefono"}) else ""),
            "section" : section_name
            }
    
    return data

def get_site_content():
    lst_data = []
    print "\n\nScrapping section(s) of %s \n\n"%(" - ".join(lst_sections))    
    for isection in lst_sections:
        page_no = 1
        results = int(re.search("\d{1,10}",get_section_content(isection,page_no).find("h1",attrs={"class":"h1Bread normalize-text"}).text).group(0))

        print "Section : %s"%(isection)
        print "Results : %s"%(results)

        while True:
            content = get_section_content(isection,page_no)

            if content:                
                lst = content.find_all("li",attrs={"class":"business"})

                print "Page #:%s \n"%(page_no)
                
                for i in lst:
                    data  = fetch_data(i,isection)
                    lst_data.append(data)
                    print "--------------------------------"
                    print "%(name)s \n%(address)s \n%(location)s \nSite:%(url)s \tags:%(tags)s \nPhone:%(phone)s"%(data)

                page_no +=1
            else:
                break
    
    return {"data":lst_data}

if __name__ == "__main__":
    get_site_content()
