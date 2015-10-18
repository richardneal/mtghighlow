#
#   Scraping Utilities
#

import urllib
import logging

from bs4 import BeautifulSoup

def getGoldfishFormatCards(format,paper):
    a=[]
    goldfishURL = "http://www.mtggoldfish.com/index/" + format
    htmlFile = urllib.urlopen(goldfishURL)
    rawHTML = htmlFile.read()
    soup = BeautifulSoup(rawHTML, "lxml")
    if not paper:
        category = soup.find("div","index-price-table-online")
    else:
        category = soup.find("div","index-price-table-paper")
    tablebody = category.find("tbody")

    for index, card in enumerate(tablebody.findAll("tr")):
        a.append([])
        values = card.findAll("td")
        for value in (values[0], values[1], values[3]):
            thestrings = [unicode(s) for s in value.findAll(text=True)]
            thetext = ''.join(thestrings)
            thetext.replace('\n','')
            thetext.replace('PRM-GPP','GPX')
            a[-1].append(thetext)
        if index > 100:
            break
    return a

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
    rawHTML = htmlFile.read()
    startURLIndex = rawHTML.find("http://magiccards.info/scans")
    endURLIndex = rawHTML.find("\"", startURLIndex)
    imageURL = rawHTML[startURLIndex:endURLIndex]
    return [imageURL]