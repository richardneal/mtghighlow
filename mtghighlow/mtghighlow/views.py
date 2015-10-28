from flask import Flask, render_template, g, session, request, jsonify
from mtghighlow import app
from mtghighlow.classes import Card, Streak, HighLowJsonEncoder, HighLowJsonDecoder

app.json_encoder = HighLowJsonEncoder
app.json_decoder = HighLowJsonDecoder

@app.route('/', methods=['GET'])
def index():
    streak = session.get('streak', Streak())
    cardlist = streak.q
    session["streak"] = streak
    return render_template('index.html', cards=cardlist, beststreak=streak.beststreak, streak=streak.streak)

@app.route('/newcard')
def newcard():
    print request.args
    choice = request.args.get('choice', 'error')
    streak = session["streak"]
    currentcard, newcard, beststreak, correct = streak.new_card(choice)
    print 'Best Streak = ' + str(beststreak)
    session["streak"] = streak
    return jsonify({"newcard":newcard, "streak":streak.streak, "currentcard":currentcard, "beststreak":beststreak, "correct":correct})