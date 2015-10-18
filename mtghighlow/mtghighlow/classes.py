from scraper import getCFBPrice, getGoldfishTopCards, getCardImageURL, getGoldfishFormatCards
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
            self.q.pop(0)
            currentcard = self.q[0]
            if result == "Higher":
                if currentcard.fakeprice > currentcard.realprice:
                    correct = "WRONG"
                    self.streak = 0
                elif currentcard.fakeprice < currentcard.realprice:
                    correct = "CORRECT"
                    self.streak += 1
            elif result == "Lower":
                if currentcard.fakeprice < currentcard.realprice:
                    correct = "WRONG"
                    self.streak = 0
                elif currentcard.fakeprice > currentcard.realprice:
                    correct = "CORRECT"
                    self.streak += 1
        print self.streak
        if self.beststreak < self.streak:
            self.beststreak = self.streak

        new = random.choice(self.allcards)
        newcard = Card(cardname=new[0], cardset=new[1], realprice=new[2])
        self.q.append(newcard)

        return self.q[0], newcard

class Card:
    def __init__(self, cardset, cardname, realprice=None, fakeprice=None, image=None):
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
            fakepricefloat = float(self.realprice)*(1 + .01 * random.randrange(-90,100))
            self.fakeprice = '{:0,.2f}'.format(fakepricefloat)

        if image:
            self.image = image
        else:
            self.image = getCardImageURL(cardname, cardset)[0]
