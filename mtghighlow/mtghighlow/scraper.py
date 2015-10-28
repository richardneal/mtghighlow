#
#   Scraping Utilities
#

import urllib
import logging

from bs4 import BeautifulSoup
import sqlite3
import os
import time

def connect_db():
    dir = os.path.dirname(__file__)
    print str(dir)
    filename = os.path.join(dir, 'db\cards.db')
    return sqlite3.connect(filename)

def archive_db():
    dir = os.path.dirname(__file__)
    print str(dir)
    filename = os.path.join(dir, 'db\cards.db')
    if not os.path.isdir(dir+'\\db\\archive\\'):
        os.makedirs(dir+'\\db\\archive\\')
    if os.path.isfile(filename):
        try:
            newfilename = dir+'\\db\\archive\\cardsarchive'+time.strftime("%Y%m%d-%H%M%S")+'.db'
            print newfilename
            os.rename(filename, newfilename)
        except Exception as e:
            print e
            return False
    open(filename, 'a').close()
    return True

def goldfishToDB(cardlist):
    if archive_db():
        conn = connect_db()
        c = conn.cursor()
        c.executescript('drop table if exists cardlist')
        c.executescript('''create table cardlist
                (name text, fullsetname text, setname text, price real)''')
        for item in cardlist:
            c.execute('insert into cardlist values (?,?,?,?)', item)
        conn.commit()
        for row in c.execute('SELECT * FROM cardlist'):
            print row
        conn.close()
    else:
        print 'Could not refresh DB'


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def getGoldfishFormatCards(format,paper):
    a=[]
    goldfishURL = "http://www.mtggoldfish.com/index/" + format
    htmlFile = urllib.urlopen(goldfishURL)
    rawHTML = htmlFile.read()
    soup = BeautifulSoup(rawHTML, "lxml")
    if paper:
        category = soup.find("div","index-price-table-paper")
    else:
        category = soup.find("div","index-price-table-online")
    tablebody = category.find("tbody")

    for index, card in enumerate(tablebody.findAll("tr")):
        info = []
        values = card.findAll("td")
        for value in (values[0], values[1], values[3]):
            thetext = u''.join(value.findAll(text=True)).strip()
            if 'PRM-GPP' in thetext:
                thetext = thetext.replace('PRM-GPP','GPX')
            info.append(thetext)
        a.append(info)
        if index > 100:
            break
    return a

def getCardlistFromDB():
    conn = connect_db()
    c = conn.cursor()
    cardlist = c.execute('select * from cardlist order by random() limit 100').fetchall()
    for card in cardlist:
        print card
    conn.close()
    return cardlist;
    
def convertSetname(name):
    if name == u'PRM-CHP':
        return 'CP'
    elif name == 'PRM-FNM':
        return 'FNMP'
    elif name == 'PRM-GDP' or name == 'PRM-MSC':
        return 'MGDC'
    elif name == 'PRM-GWP' or name == 'PRM-WPN':
        return 'GRC'
    elif name == 'PRM-GPP':
        return 'GPX'
    elif name == 'PRM-JSS':
        return 'SUS'
    elif name == 'PRM-JUD':
        return 'JR'
    elif name == 'PRM-LPC':
        return 'MLP'
    elif name == 'PRM-MPR':
        return 'MPRP'
    elif name == 'PRM-MED':
        return 'MBP'
    elif name == 'PRM-PRE':
        return 'PTC'
    elif name == 'PRM-PTP':
        return 'PRO'
    elif name == 'PRM-REL':
        return 'REP'
    elif name == 'PRM-SPO':
        return 'UQC'
    else:
        return name

def getGoldfishTotalCards (paper):
    a = []
    if paper:
        goldfishURL = "http://www.mtggoldfish.com/prices/paper/"
    else:
        goldfishURL = "http://www.mtggoldfish.com/prices/online/"
    
    for format in ['standard', 'modern_two', 'modern_one', 'legacy_two', 'legacy_one', 'special']:
        htmlFile = urllib.urlopen(goldfishURL+format)
        rawHTML = htmlFile.read()
        soup = BeautifulSoup(rawHTML, "html.parser")
        sets = soup.findAll("div", {"class":"priceList-set"})
        print len(sets)
        for set in sets:
            try:
                info = []
                setname = convertSetname(set.find('a', {"class" : "priceList-set-header-link"}, href=True, text=True)['href'][7:])
                fullsetname = set.find('a', {"class" : "priceList-set-header-link"}, href=True, text=True).contents[0]
                print fullsetname + ', ' + setname
                cards = [card.find(text=True).strip() for card in set.findAll('dt')]
                prices = [card.find(text=True).strip().replace(',', '') for card in set.findAll("div", {"class" : "priceList-price-price-wrapper"})]
                if (len(cards) == len(prices)):
                    setarray = [setname]*len(cards)
                    fullsetarray = [fullsetname]*len(cards)
                    info = zip(cards, fullsetarray, setarray, prices)
                else:
                    print "There was an error with the card list not matching length of prices"

                a.extend(info)
            except Exception as e:
                pass

    goldfishToDB(a)

def getGoldfishTopCards():
    goldfishURL = "http://www.mtggoldfish.com/format-staples/standard/full/all"
    htmlFile = urllib.urlopen(goldfishURL)
    rawHTML = htmlFile.read()
    endIndex = 1
    cards = []
    for i in range(50):
        firstIndex = rawHTML.find('href="/price/', endIndex)
        secondIndex = rawHTML.find('/', firstIndex+12)
        thirdIndex = rawHTML.find('/', secondIndex+1)
        endIndex = rawHTML.find('"', thirdIndex+1)
        cards.append([rawHTML[secondIndex+1:thirdIndex].replace('+', ' ')])
        cards[-1].append(rawHTML[thirdIndex+1:endIndex].replace('+', ' '))
    return cards

#
#   Retrieves a URL to the card's image as represented by http://magiccards.info
#
def getCardImageURL(cardName, cardSet):
    magicInfoURL = "http://magiccards.info/query?q=" + urllib.quote(cardName)
    if cardSet:
        magicInfoURL += urllib.quote(" e:" + cardSet + "/en")
    htmlFile = urllib.urlopen(magicInfoURL)
    rawHTML = htmlFile.read() # add error handling
    startURLIndex = rawHTML.find("http://magiccards.info/scans")
    endURLIndex = rawHTML.find("\"", startURLIndex)
    imageURL = rawHTML[startURLIndex:endURLIndex]
    if imageURL == '':
        imageURL = ["../static/img/mtgback.jpg"]
    return imageURL