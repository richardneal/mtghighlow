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
    if "streak" in session:
        streak = classes.Streak(session["streak"])
    else:
        streak = classes.Streak()

    cardlist = []
    for i in range(streak.maxlength):
        cardlist.append(streak.new_card()[1])
    session["streak"] = streak
    return render_template('index.html', cards=cardlist)

@app.route('/newcard')
def newcard():
    higher = "Higher" if request.args.get('higher') == 'true' else "Lower"
    streak = classes.Streak(session["streak"])
    currentcard, newcard, beststreak = streak.new_card(higher)
    print 'Best Streak = ' + str(beststreak)
    session["streak"] = streak
    return jsonify({"newcard":newcard, "streak":streak.streak, "currentcard":currentcard, "beststreak":beststreak})