from flask import Flask, render_template, g, session, request
from flask.json import JSONEncoder
from mtghighlow import app, classes

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, classes.Streak):
            return {
                'cards': obj.cards, 
                'currentcard': obj.currentcard,
                'streak': obj.streak,
                'beststreak': obj.beststreak,
            }
        elif isinstance(obj, classes.Card):
            return {
                'cardset': obj.cardset, 
                'cardname': obj.cardname,
                'realprice': obj.realprice,
                'fakeprice': obj.fakeprice,
            }
        return super(MyJSONEncoder, self).default(obj)


app.json_encoder = MyJSONEncoder

@app.route('/', methods=['GET', 'POST'])
def index():
    result = 'None'
    if request.method == 'POST':
        if 'higherbutton' in request.form.keys():
            result = 'Higher'
        elif 'lowerbutton' in request.form.keys():
            result = 'Lower'
    if not hasattr(g, "streak"):
        streak = classes.Streak()
    else:
        streak = classes.Streak(g.streak)
        
    correct = streak.new_card(result)
    g.streak = streak

    if request.method == 'POST':
        return render_template('index.html', nameold=streak.lastcard.cardname, namenew=streak.currentcard.cardname, result=result, imageurl=streak.currentcard.image, streak=streak.streak, realpriceold=streak.lastcard.realprice, fakepriceold=streak.lastcard.fakeprice, fakepricenew=streak.currentcard.fakeprice, correct=correct, beststreak=streak.beststreak)
    else:
        return render_template('index.html', nameold=None, namenew=streak.currentcard.cardname, result=result, imageurl=streak.currentcard.image, streak=streak.streak, realpriceold=None, fakepriceold=None, fakepricenew=streak.currentcard.fakeprice, correct=correct, beststreak=streak.beststreak)

@app.before_request
def load_streak():
    if "streak" in session:
        g.streak = session["streak"]

@app.after_request
def serialize_streak(response):
    if hasattr(g, "streak"):
        session["streak"] = g.streak
    return response
