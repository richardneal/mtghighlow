from mtghighlow.scraper import getCardImageURL, getCardlistFromDB
from random import uniform
from flask.json import JSONEncoder, JSONDecoder

class Streak:
    def __init__(self, allcards = None, streak = None, beststreak = None, q = None, rarity=None, format=None, difficulty=None):
        self.maxlength = 5
        self.streak = streak if streak else 0
        self.beststreak = beststreak if beststreak else 0
        self.rarity = rarity if rarity else ['Mythic','Rare','Uncommon','Common']
        self.format = format if format else ['standard','modern','legacy','special']
        self.difficulty = difficulty if difficulty else ['easy']
        self.allcards = allcards if allcards else getCardlistFromDB(self.rarity,self.format)

        if q:
            self.q = q
        else:
            self.q = []
            for i in range(self.maxlength):
                card = self.allcards.pop(0)
                self.q.append(Card(cardname=card[0], cardsetfull=card[1], cardset=card[2], realprice=card[3], rarity=card[4]))

    def new_card(self, choice = None):
        result = 0
        currentcard = None
        if choice:
            print("choice: " + choice)
            currentcard = self.q.pop(0)
            try:
                currentcard.fakeprice = float(currentcard.fakeprice)
                currentcard.realprice = float(currentcard.realprice)
            except:
                currentcard.realprice = -1.0
                currentcard.fakeprice = -1.0
            if choice == "error":
                print("Error in choice! Real Price: "+ str(currentcard.realprice) + " Fake Price: " + str(currentcard.fakeprice))
            elif abs(currentcard.fakeprice - currentcard.realprice) < .1 and choice == 'lucky':
                result = 'lucky'
                print("LUCKY!: You Selected Lucky, and Real Price: " + str(currentcard.realprice) + " was within .10 of Fake Price: " + str(currentcard.fakeprice) + ". +10 Points!")
                self.streak += 10
            elif currentcard.fakeprice > currentcard.realprice:
                if choice == "lower":
                    result = 'correct'
                    print("CORRECT: You Selected Lower, and Real Price: " + str(currentcard.realprice) + " was Lower than Fake Price: " + str(currentcard.fakeprice))
                    self.streak += 1
                elif choice == "higher":
                    result = 'wrong'
                    print("WRONG: You Selected Higher, and Real Price: " + str(currentcard.realprice) + " was Lower than Fake Price: " + str(currentcard.fakeprice))
                    self.streak = 0
                elif choice == "lucky":
                    result = 'notlucky'
                    print("NOT SO LUCKY: You Selected Lucky, and Real Price: " + str(currentcard.realprice) + " was Lower than Fake Price: " + str(currentcard.fakeprice))
                    self.streak = 0
            elif currentcard.fakeprice < currentcard.realprice:
                if choice == "higher":
                    result = 'correct'
                    print("CORRECT: You Selected Higher, and Real Price: " + str(currentcard.realprice) + " was Greater than Fake Price: " + str(currentcard.fakeprice))
                    self.streak += 1
                elif choice == "lower":
                    result = 'wrong'
                    print("WRONG: You Selected Lower, and Real Price: " + str(currentcard.realprice) + " was Greater than Fake Price: " + str(currentcard.fakeprice))
                    self.streak = 0
                elif choice == "lucky":
                    result = 'notlucky'
                    print("NOT SO LUCKY: You Selected Lucky, and Real Price: " + str(currentcard.realprice) + " was Greater than Fake Price: " + str(currentcard.fakeprice))
                    self.streak = 0
            elif currentcard.fakeprice == currentcard.realprice:
                if currentcard.fakeprice == -1.0:
                    result = 'error'
                    print("There was an error in converting your Real or Fake price, your streak should be unaffected.")
                elif choice == "higher":
                    result = 'tricked'
                    print("TRICKED: You Selected Higher, and Real Price: " + str(currentcard.realprice) + " was exactly Fake Price: " + str(currentcard.fakeprice) + ". Streak Unaffected")
                    self.streak += 0
                elif choice == "lower":
                    result = 'tricked'
                    print("TRICKED: You Selected Lower, and Real Price: " + str(currentcard.realprice) + " was excatly Fake Price: " + str(currentcard.fakeprice) + ". Streak Unaffected")
                    self.streak += 0
        print(self.streak)
        if self.beststreak < self.streak:
            self.beststreak = self.streak
        print(self.beststreak)

        if len(self.allcards) < 10:
            self.allcards.extend(getCardlistFromDB(self.rarity,self.format))

        bottom = self.allcards.pop(0)
        bottomcard = Card(cardname=bottom[0], cardsetfull=bottom[1], cardset=bottom[2], realprice=bottom[3], rarity=bottom[4])
        self.q.append(bottomcard)

        self.q[0].getfakeprice(self.streak)

        return self.q[0], bottomcard, self.beststreak, result

class Card:
    def __init__(self, cardset = None, cardsetfull = None, cardname = None, realprice = 0, fakeprice = 0, image = None, rarity = None):
        self.cardset = cardset if cardset else ''
        self.cardsetfull = cardsetfull if cardsetfull else ''
        self.cardname = cardname if cardname else ''
        self.realprice = realprice if realprice else -1.0
        self.image = image if image else getCardImageURL(cardname, cardset)
        self.rarity = rarity if rarity else ''

        if fakeprice:
            self.fakeprice = fakeprice
        else:
            self.getfakeprice(1)

    def getfakeprice(self, streak, difficulty = 'easy'):
        if difficulty is 'easy':
            multiplier = 1 + uniform((-0.985**streak), (0.985**streak))
        elif difficulty is 'medium':
            multiplier = 1 + uniform((-0.75**streak), (0.75**streak))
        elif difficulty is 'hard':
            multiplier = 1 + uniform((-0.5**streak), (0.5**streak))
        self.fakeprice = float(self.realprice) * multiplier

class HighLowJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Streak):
            return {
                'allcards': obj.allcards, 
                'streak': obj.streak,
                'beststreak': obj.beststreak,
                'rarity':obj.rarity,
                'difficulty':obj.difficulty,
                'format':obj.format,
                'q': obj.q,
            }
        elif isinstance(obj, Card):
            return {
                'cardset': obj.cardset,
                'cardsetfull': obj.cardsetfull, 
                'cardname': obj.cardname,
                'realprice': obj.realprice,
                'fakeprice': obj.fakeprice,
                'image': obj.image,
                'rarity': obj.rarity,
            }
        try:
            return super().default(obj.decode())
        except AttributeError:
            return super().default(obj)

class HighLowJsonDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        kwargs['object_hook'] = self.deserialize
        JSONDecoder.__init__(self,  *args, **kwargs)

    def deserialize(self, d): 
        if 'allcards' in d:
            return Streak(**d)
        elif 'cardname' in d:
            return Card(**d)
        else:
            return d