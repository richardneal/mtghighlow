from flask import Flask, render_template, g, session, request, jsonify
from flask.json import JSONEncoder
from mtghighlow import app, classes

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, classes.Streak):
            return {
                'allcards': obj.allcards, 
                'streak': obj.streak,
                'beststreak': obj.beststreak,
                'queue': obj.q,
            }
        elif isinstance(obj, classes.Card):
            return {
                'cardset': obj.cardset, 
                'cardname': obj.cardname,
                'realprice': obj.realprice,
                'fakeprice': obj.fakeprice,
                'image': obj.image,
            }
        return super(MyJSONEncoder, self).default(obj)


app.json_encoder = MyJSONEncoder

@app.route('/', methods=['GET'])
def index():
    if request.method == 'POST':
        if 'higherbutton' in request.form.keys():
            result = 'Higher'
        elif 'lowerbutton' in request.form.keys():
            result = 'Lower'
    if not hasattr(g, "streak"):
        streak = classes.Streak()
    else:
        streak = classes.Streak(g.streak)
        
    g.streak = streak

    cardlist = []
    for i in range(streak.maxlength):
        cardlist.append(streak.new_card()[1])

    if request.method == 'GET':
        #return render_template('index.html', nameold=streak.lastcard.cardname, namenew=streak.currentcard.cardname, result=result, imageurl=streak.currentcard.image, streak=streak.streak, realpriceold=streak.lastcard.realprice, fakepriceold=streak.lastcard.fakeprice, fakepricenew=streak.currentcard.fakeprice, correct=correct, beststreak=streak.beststreak)
        return render_template('index.html', cards=cardlist)
    #else:
    #    #return render_template('index.html', nameold=None, namenew=streak.currentcard.cardname, result=result, imageurl=streak.currentcard.image, streak=streak.streak, realpriceold=None, fakepriceold=None, fakepricenew=streak.currentcard.fakeprice, correct=correct, beststreak=streak.beststreak)
    #    return render_template('index.html', cards=[streak.currentcard])

@app.before_request
def load_streak():
    if "streak" in session:
        g.streak = session["streak"]

@app.after_request
def serialize_streak(response):
    if hasattr(g, "streak"):
        session["streak"] = g.streak
    return response

@app.route('/newcard')
def newcard():
    higher = "Higher" if request.args.get('higher') == 'true' else "Lower"
    streak = classes.Streak(g.streak)
    currentcard, newcard = streak.new_card(higher)
    g.streak = streak
    return jsonify({"newcard":newcard, "streak":streak.streak, "currentcard":currentcard})