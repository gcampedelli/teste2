import scraperwiki
import lxml.etree
import lxml.html
import time 
import re
from datetime import date, timedelta

def scrapeTable(root, numId):
    
    #annonces
    for annonce in root.cssselect("table"):

        #enregistrement des resultats
        record = {}      
        
        for uneAnnonce in annonce.cssselect("table tr.odd"):

            #job url
            for jobUrl in uneAnnonce.cssselect("a"):
                record["url"]=jobUrl.get('href')
                
            print 'url : ', record["url"]

            #email
            for email in uneAnnonce.cssselect("td"):
                record["email"]=email.text
        
            #save in datastore
            scraperwiki.sqlite.save(["id"], record)
            numId=numId+1

        for uneAnnonce in annonce.cssselect("table tr.even"):
            #job url
            for jobUrl in uneAnnonce.cssselect("a"):
                record["url"]=jobUrl.get('href')
                
            print 'url : ', record["url"]
        
            #salaire
            for email in uneAnnonce.cssselect("div.companyContainer div.fnt13"):
                record["email"]=email.text
        
            #id
            record["id"]=numId
            
            #print record["region"]
    
            #save in datastore
            scraperwiki.sqlite.save(["id"], record)
            numId=numId+1



#start
sUrlBase="https://www.secom.planalto.gov.br/consea/boletins.nsf/01ContatoxNome?OpenView&Start="
numId=0

for page in range(50):
    page=page+30
    sUrl=sUrlBase + str(page) + "&cy=LU"
    print sUrl

    html = scraperwiki.scrape(sUrl)
    root = lxml.html.fromstring(html)

    scrapeTable(root, numId)
    numId=numId+20 
