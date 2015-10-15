from scraper import getCFBPrice, getGoldfishTopCards, getCardImageURL
import random

class Streak:
    def __init__(self, serialized_dict=None):
        if serialized_dict:
            self.cards = serialized_dict['cards']
            self.lastcard = Card(serialized_dict['currentcard']['cardset'], serialized_dict['currentcard']['cardname'], serialized_dict['currentcard']['realprice'], serialized_dict['currentcard']['fakeprice'])
            self.streak = serialized_dict['streak']
            self.beststreak = serialized_dict['beststreak']
        else:
            self.cards = getGoldfishTopCards()
            self.currentcard = None
            self.streak = 0
            self.beststreak = 0
            self.lastcard = None

    def new_card(self, card, result):
        correct = 0
        if result == "Higher":
            if card.fakeprice > card.realprice:
                correct = "WRONG"
                self.streak = 0
            elif card.fakeprice < card.realprice:
                correct = "CORRECT"
                self.streak += 1
        elif result == "Lower":
            if card.fakeprice < card.realprice:
                correct = "WRONG"
                self.streak = 0
            elif card.fakeprice > card.realprice:
                correct = "CORRECT"
                self.streak += 1
        print self.streak
        if self.beststreak < self.streak:
            self.beststreak = self.streak
        card = random.choice(self.cards)

        self.currentcard = Card(card[0], card[1])
        return self.currentcard

class Card:
    def __init__(self, cardset, cardname, realprice=None, fakeprice=None):
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


        self.image = getCardImageURL(cardname, None)[0]
