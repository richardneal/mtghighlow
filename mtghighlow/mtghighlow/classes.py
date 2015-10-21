﻿from scraper import getGoldfishTopCards, getCardImageURL, getGoldfishFormatCards
import random

class Streak:
    def __init__(self, serialized_dict=None):
        self.maxlength = 5
        self.q = []
        try:
            self.allcards = serialized_dict['allcards']
            self.streak = serialized_dict['streak']
            self.beststreak = serialized_dict['beststreak']
            for elem in serialized_dict['queue']:
                self.q.append(Card(elem["cardset"], elem["cardname"], elem["realprice"], elem["fakeprice"], elem["image"]))
                if len(self.q) > self.maxlength:
                    self.q.pop(0)
        except Exception as e:
            print str(e)
            self.allcards = getGoldfishFormatCards("modern", True)
            self.streak = 0
            self.beststreak = 0

            print "done"

    def new_card(self, result = None):
        correct = 0
        currentcard = None
        if result:
            print "result: " + result
            currentcard = self.q.pop(0)
            try:
                currentcard.fakeprice = float(currentcard.fakeprice)
                currentcard.realprice = float(currentcard.realprice)
            except:
                currentcard.realprice = -1.0
                currentcard.fakeprice = -1.0
            if currentcard.fakeprice > currentcard.realprice:
                if result == "Higher":
                    correct = False
                    print "WRONG: You Selected Higher, and the Fake Price: " + str(currentcard.fakeprice) + " was greater than Real Price: " + str(currentcard.realprice)
                    self.streak = 0
                elif result == "Lower":
                    correct = True
                    print "Correct: You Selected Lower, and the Fake Price: " + str(currentcard.fakeprice) + " was Greater than Real Price: " + str(currentcard.realprice)
                    self.streak += 1
            if currentcard.fakeprice < currentcard.realprice:
                if result == "Lower":
                    correct = False
                    print "WRONG: You Selected Lower, and the Fake Price: " + str(currentcard.fakeprice) + " was Lower than Real Price: " + str(currentcard.realprice)
                    self.streak = 0
                elif result == "Higher":
                    correct = True
                    print "Correct: You Selected Higher, and the Fake Price: " + str(currentcard.fakeprice) + " was less than Real Price: " + str(currentcard.realprice)
                    self.streak += 1
            if currentcard.fakeprice == -1.0 or currentcard.realprice == -1.0:
                correct = "ERROR"
                print "There was an error, your streak should be unaffected."
        print self.streak
        if self.beststreak < self.streak:
            self.beststreak = self.streak
        print self.beststreak

        bottom = random.choice(self.allcards)
        bottomcard = Card(cardname=bottom[0], cardset=bottom[1], realprice=bottom[2])
        self.q.append(bottomcard)

        self.q[0].getfakeprice(self.streak)

        return self.q[0], bottomcard, self.beststreak, correct

class Card:
    def __init__(self, cardset, cardname, realprice=0, fakeprice=0, image=None):
        self.cardset = cardset
        self.cardname = cardname

        if realprice:
            self.realprice = realprice
        else:
            try:
                self.realprice = float(getCFBPrice(cardname, cardset)[0])
            except:
                self.realprice = -1.0

        if fakeprice:
            self.fakeprice = fakeprice
        else:
            self.getfakeprice(1)

        if image:
            self.image = image
        else:
            self.image = getCardImageURL(cardname, cardset)[0]

    def getfakeprice(self, streak):
        multiplier = 1 + random.uniform((-0.985**streak), (0.985**streak))
        fakepricefloat = float(self.realprice) * multiplier
        self.fakeprice = '{:0,.2f}'.format(fakepricefloat)

