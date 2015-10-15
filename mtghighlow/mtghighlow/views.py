from flask import Flask, render_template, g, session, request, jsonify
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
                'image': obj.image,
            }
        return super(MyJSONEncoder, self).default(obj)


app.json_encoder = MyJSONEncoder

@app.route('/', methods=['GET'])
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
        
    correct = streak.new_card(result, None)
    g.streak = streak

    cardlist = []
    for i in range(4):
        streak.new_card(False, None)
        cardlist.append(streak.currentcard)

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
    currentcard = classes.Card(request.args['currentcard[cardset]'], request.args['currentcard[cardname]'], request.args['currentcard[realprice]'], request.args['currentcard[fakeprice]'])
    higher = "Higher" if request.args.get('higher') == 'true' else "Lower"
    streak = classes.Streak(g.streak)
    streak.new_card(currentcard, higher)
    return jsonify({"newcard":streak.currentcard, "streak":streak.streak})