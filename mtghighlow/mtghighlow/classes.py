from mtghighlow.scraper import get_image_url, get_cardlist_from_db
from random import uniform
from flask.json import JSONEncoder, JSONDecoder
from enum import Enum

class Streak:
    def __init__(self, all_cards=None, current_streak_length=None, best_streak_length=None, queue=None, rarity=None, format=None, difficulty=None):
        self.max_queue_length = 5
        self.current_streak_length = current_streak_length if current_streak_length else 0
        self.best_streak_length = best_streak_length if best_streak_length else 0
        self.rarity = rarity if rarity else [rarity for rarity in Rarities.__members__.keys()]
        self.format = format if format else ['standard','modern','legacy','special']
        self.difficulty = difficulty if difficulty else Difficulties.Easy
        self.all_cards = all_cards if all_cards else get_cardlist_from_db(self.rarity, self.format)

        if queue:
            self.queue = queue
        else:
            self.queue = []
            for i in range(self.max_queue_length):
                card = self.all_cards.pop(0)
                self.queue.append(Card(name=card[0], set_full=card[1], set=card[2], real_price=card[3], rarity=card[4]))

    def new_card(self, choice=None):
        result = Results.Error
        current_card = None
        if choice:
            print("choice: " + choice)
            current_card = self.queue.pop(0)
            try:
                current_card.fake_price = float(current_card.fake_price)
                current_card.real_price = float(current_card.real_price)
            except:
                current_card.real_price = -1.0
                current_card.fake_price = -1.0
            if choice == "error":
                print("Error in choice! Real Price: " + str(current_card.real_price) + " Fake Price: " + str(current_card.fake_price))
            elif abs(current_card.fake_price - current_card.real_price) < .1 and choice == 'lucky':
                result = Results.Lucky
                print("LUCKY!: You Selected Lucky, and Real Price: " + str(current_card.real_price) + " was within .10 of Fake Price: " + str(current_card.fake_price) + ". +10 Points!")
                self.current_streak_length += 10
            elif current_card.fake_price > current_card.real_price:
                if choice == "lower":
                    result = Results.Correct
                    print("CORRECT: You Selected Lower, and Real Price: " + str(current_card.real_price) + " was Lower than Fake Price: " + str(current_card.fake_price))
                    self.current_streak_length += 1
                elif choice == "higher":
                    result = Results.Incorrect
                    print("WRONG: You Selected Higher, and Real Price: " + str(current_card.real_price) + " was Lower than Fake Price: " + str(current_card.fake_price))
                    self.current_streak_length = 0
                elif choice == "lucky":
                    result = Results.Unlucky
                    print("NOT SO LUCKY: You Selected Lucky, and Real Price: " + str(current_card.real_price) + " was Lower than Fake Price: " + str(current_card.fake_price))
                    self.current_streak_length = 0
            elif current_card.fake_price < current_card.real_price:
                if choice == "higher":
                    result = Results.Correct
                    print("CORRECT: You Selected Higher, and Real Price: " + str(current_card.real_price) + " was Greater than Fake Price: " + str(current_card.fake_price))
                    self.current_streak_length += 1
                elif choice == "lower":
                    result = Results.Incorrect
                    print("WRONG: You Selected Lower, and Real Price: " + str(current_card.real_price) + " was Greater than Fake Price: " + str(current_card.fake_price))
                    self.current_streak_length = 0
                elif choice == "lucky":
                    result = Results.Unlucky
                    print("NOT SO LUCKY: You Selected Lucky, and Real Price: " + str(current_card.real_price) + " was Greater than Fake Price: " + str(current_card.fake_price))
                    self.current_streak_length = 0
            elif current_card.fake_price == current_card.real_price:
                if current_card.fake_price == -1.0:
                    result = Results.Error
                    print("There was an error in converting your Real or Fake price, your streak should be unaffected.")
                elif choice == "higher":
                    result = Results.Tricked
                    print("TRICKED: You Selected Higher, and Real Price: " + str(current_card.real_price) + " was exactly Fake Price: " + str(current_card.fake_price) + ". Streak Unaffected")
                    self.current_streak_length += 0
                elif choice == "lower":
                    result = Results.Tricked
                    print("TRICKED: You Selected Lower, and Real Price: " + str(current_card.real_price) + " was excatly Fake Price: " + str(current_card.fake_price) + ". Streak Unaffected")
                    self.current_streak_length += 0
        print(self.current_streak_length)
        if self.best_streak_length < self.current_streak_length:
            self.best_streak_length = self.current_streak_length
        print(self.best_streak_length)

        if len(self.all_cards) < 10:
            self.all_cards.extend(get_cardlist_from_db(self.rarity,self.format))

        bottom = self.all_cards.pop(0)
        bottomcard = Card(name=bottom[0], set_full=bottom[1], set=bottom[2], real_price=bottom[3], rarity=bottom[4])
        self.queue.append(bottomcard)

        self.queue[0].get_multiplier(self.current_streak_length)

        return self.queue[0], bottomcard, self.best_streak_length, result

class Card:
    def __init__(self, set=None, set_full=None, name=None, real_price=0, fake_price=0, image=None, rarity=None):
        self.set = set if set else ''
        self.set_full = set_full if set_full else ''
        self.name = name if name else ''
        self.real_price = real_price if real_price else -1.0
        self.image = image if image else get_image_url(name, set)
        self.rarity = rarity if rarity else ''

        if fake_price:
            self.fake_price = fake_price
        else:
            self.fake_price = float(self.real_price) * self.get_multiplier(1)

    def get_multiplier(self, streak, difficulty='easy'):
        if difficulty is 'easy':
            multiplier = 1 + uniform((-0.985 ** streak), (0.985 ** streak))
        elif difficulty is 'medium':
            multiplier = 1 + uniform((-0.75 ** streak), (0.75 ** streak))
        elif difficulty is 'hard':
            multiplier = 1 + uniform((-0.5 ** streak), (0.5 ** streak))
        return multiplier

class HighLowJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Streak):
            return {
                'all_cards': obj.all_cards, 
                'current_streak_length': obj.current_streak_length,
                'best_streak_length': obj.best_streak_length,
                'rarity':obj.rarity,
                'difficulty':obj.difficulty,
                'format':obj.format,
                'queue': obj.queue,
            }
        elif isinstance(obj, Card):
            return {
                'set': obj.set,
                'set_full': obj.set_full, 
                'name': obj.name,
                'real_price': obj.real_price,
                'fake_price': obj.fake_price,
                'image': obj.image,
                'rarity': obj.rarity,
            }
        elif isinstance(obj, Enum):
            return obj.name
        try:
            return super().default(obj.decode())
        except AttributeError:
            return super().default(obj)

class HighLowJsonDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        kwargs['object_hook'] = self.deserialize
        JSONDecoder.__init__(self,  *args, **kwargs)

    def deserialize(self, d): 
        if 'all_cards' in d:
            return Streak(**d)
        elif 'name' in d:
            return Card(**d)
        else:
            return d

class Rarities(Enum):
    Common = "Common"
    Uncommon = "Uncommon"
    Rare = "Rare"
    Mythic = "Mythic"

class Results(Enum):
    Lucky = "Lucky"
    Unlucky = "Unlucky"
    Incorrect = "Incorrect"
    Correct = "Correct"
    Tricked = "Tricked"
    Error = "Error"

class Difficulties(Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"

class Formats(Enum):
    Standard = "standard"
