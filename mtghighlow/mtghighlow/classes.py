from scraper import getCardImageURL, getCardlistFromDB
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
            self.allcards = getCardlistFromDB()
            print "all cards type is:" + str(type(self.allcards))
            self.streak = 0
            self.beststreak = 0

            print "done"

    def new_card(self, choice = None):
        result = 0
        currentcard = None
        if choice:
            print "choice: " + choice
            currentcard = self.q.pop(0)
            try:
                currentcard.fakeprice = float(currentcard.fakeprice)
                currentcard.realprice = float(currentcard.realprice)
            except:
                currentcard.realprice = -1.0
                currentcard.fakeprice = -1.0
            if choice == "error":
                print "Error in choice! Real Price: "+ str(currentcard.realprice) + " Fake Price: " + str(currentcard.fakeprice)
            elif abs(currentcard.fakeprice - currentcard.realprice) < .1 and choice == 'lucky':
                result = 'lucky'
                print "LUCKY!: You Selected Lucky, and Real Price: " + str(currentcard.realprice) + " was within .10 of Fake Price: " + str(currentcard.fakeprice) + ". +10 Points!"
                self.streak += 10
            elif currentcard.fakeprice > currentcard.realprice:
                if choice == "lower":
                    result = 'correct'
                    print "CORRECT: You Selected Lower, and Real Price: " + str(currentcard.realprice) + " was Lower than Fake Price: " + str(currentcard.fakeprice)
                    self.streak += 1
                elif choice == "higher":
                    result = 'wrong'
                    print "WRONG: You Selected Higher, and Real Price: " + str(currentcard.realprice) + " was Lower than Fake Price: " + str(currentcard.fakeprice)
                    self.streak = 0
                elif choice == "lucky":
                    result = 'notlucky'
                    print "NOT SO LUCKY: You Selected Lucky, and Real Price: " + str(currentcard.realprice) + " was Lower than Fake Price: " + str(currentcard.fakeprice)
                    self.streak = 0
            elif currentcard.fakeprice < currentcard.realprice:
                if choice == "higher":
                    result = 'correct'
                    print "CORRECT: You Selected Higher, and Real Price: " + str(currentcard.realprice) + " was Greater than Fake Price: " + str(currentcard.fakeprice)
                    self.streak += 1
                elif choice == "lower":
                    result = 'wrong'
                    print "WRONG: You Selected Lower, and Real Price: " + str(currentcard.realprice) + " was Greater than Fake Price: " + str(currentcard.fakeprice)
                    self.streak = 0
                elif choice == "lucky":
                    result = 'notlucky'
                    print "NOT SO LUCKY: You Selected Lucky, and Real Price: " + str(currentcard.realprice) + " was Greater than Fake Price: " + str(currentcard.fakeprice)
                    self.streak = 0
            elif currentcard.fakeprice == currentcard.realprice:
                if currentcard.fakeprice == -1.0:
                    result = 'error'
                    print "There was an error in converting your Real or Fake price, your streak should be unaffected."
                elif choice == "higher":
                    result = 'tricked'
                    print "TRICKED: You Selected Higher, and Real Price: " + str(currentcard.realprice) + " was exactly Fake Price: " + str(currentcard.fakeprice) + ". Streak Unaffected"
                    self.streak += 0
                elif choice == "lower":
                    result = 'tricked'
                    print "TRICKED: You Selected Lower, and Real Price: " + str(currentcard.realprice) + " was excatly Fake Price: " + str(currentcard.fakeprice) + ". Streak Unaffected"
                    self.streak += 0
        print self.streak
        if self.beststreak < self.streak:
            self.beststreak = self.streak
        print self.beststreak

        if len(self.allcards) < 10:
            self.allcards.extend(getCardlistFromDB())

        bottom = self.allcards.pop(0)
        bottomcard = Card(cardname=bottom[0], cardset=bottom[1], realprice=bottom[2])
        self.q.append(bottomcard)

        self.q[0].getfakeprice(self.streak)

        return self.q[0], bottomcard, self.beststreak, result

class Card:
    def __init__(self, cardset, cardname, realprice=0, fakeprice=0, image=None):
        self.cardset = cardset
        self.cardname = cardname

        if realprice:
            self.realprice = realprice
        else:
            self.realprice = -1.0

        if fakeprice:
            self.fakeprice = fakeprice
        else:
            self.getfakeprice(1)

        if image:
            self.image = image
        else:
            self.image = getCardImageURL(cardname, cardset)

    def getfakeprice(self, streak):
        multiplier = 1 + random.uniform((-0.985**streak), (0.985**streak))
        #The multiplier below can be used to test tricked and lucky scenarios. lower will always be 'tricked' or 'correct', higher will always be 'tricked' or 'wrong' and middle will always be 'lucky' or 'not lucky'
        #multiplier = 1 + random.uniform(0,.005)
        self.fakeprice = float(self.realprice) * multiplier

