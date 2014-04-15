import scraperwiki
import lxml.etree
import lxml.html
import time 
import re
from datetime import date, timedelta

def scrapeTable(root, numId):
    
    #annonces
    for annonce in root.cssselect("div#primaryResults"):

        #enregistrement des resultats
        record = {}      
        
        for uneAnnonce in annonce.cssselect("table tr.odd"):

            #job url
            for jobUrl in uneAnnonce.cssselect("div.jobTitleContainer a"):
                record["url"]=jobUrl.get('href')
                
            print 'Job url : ', record["url"]

            #company name
            for nomCompany in uneAnnonce.cssselect("div.companyContainer a"):
                record["company"]=nomCompany.text
                
            #annonceName
            for annonceName in uneAnnonce.cssselect("div.jobTitleContainer a"):
                record["annonceName"]=annonceName.text
        
            #salaire
            for salaire in uneAnnonce.cssselect("div.companyContainer div.fnt13"):
                record["salaire"]=salaire.text
        
            #date
            for parution in uneAnnonce.cssselect("div.jobTitleCol div.fnt20"):
                if "Aujourd" in parution.text_content().strip().split("'")[0]:
                    record["parution"]=time.strftime('%d/%m/%y', time.localtime())
                else:
                    s = re.findall('\d+', parution.text_content().strip())
                    numDays = int(s[0])
                    print "numDays", numDays
                    d = date.today()-timedelta(days=numDays)
                    record["parution"]=d.strftime('%d/%m/%y')

            print "parution : ", record["parution"]
    
            #region
            for region in uneAnnonce.cssselect("div.jobLocationSingleLine a"):
                record["region"]=region.text
    
            #id
            record["id"]=numId

            #save in datastore
            scraperwiki.sqlite.save(["id"], record)
            numId=numId+1

        for uneAnnonce in annonce.cssselect("table tr.even"):
            #job url
            for jobUrl in uneAnnonce.cssselect("div.jobTitleContainer a"):
                record["url"]=jobUrl.get('href')
                
            print 'Job url : ', record["url"]

            #company name
            for nomCompany in uneAnnonce.cssselect("div.companyContainer a"):
                record["company"]=nomCompany.text
                
            #annonceName
            for annonceName in uneAnnonce.cssselect("div.jobTitleContainer a"):
                record["annonceName"]=annonceName.text
        
            #salaire
            for salaire in uneAnnonce.cssselect("div.companyContainer div.fnt13"):
                record["salaire"]=salaire.text
        
            #date
            for parution in uneAnnonce.cssselect("div.jobTitleCol div.fnt20"):
                if "Aujourd" in parution.text_content().strip().split("'")[0]:
                    record["parution"]=time.strftime('%d/%m/%y', time.localtime())
                else:
                    s = re.findall('\d+', parution.text_content().strip())
                    numDays = int(s[0])
                    print "numDays", numDays
                    d = date.today()-timedelta(days=numDays)
                    record["parution"]=d.strftime('%d/%m/%y')

            print "parution : ", record["parution"]
    
            #region
            for region in uneAnnonce.cssselect("div.jobLocationSingleLine a"):
                record["region"]=region.text
    
            #id
            record["id"]=numId
            
            #print record["region"]
    
            #save in datastore
            scraperwiki.sqlite.save(["id"], record)
            numId=numId+1



#start
sUrlBase="http://offres.monster.fr/offres-d-emploi/?pg="
numId=0

for page in range(40):
    page=page+1
    sUrl=sUrlBase + str(page) + "&cy=LU"
    print sUrl

    html = scraperwiki.scrape(sUrl)
    root = lxml.html.fromstring(html)

    scrapeTable(root, numId)
    numId=numId+20 
