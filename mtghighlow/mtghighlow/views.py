from flask import Flask, render_template, g, session, request, jsonify
from mtghighlow import app
from mtghighlow.classes import Card, Streak, HighLowJsonEncoder, HighLowJsonDecoder

app.json_encoder = HighLowJsonEncoder
app.json_decoder = HighLowJsonDecoder

@app.route('/', methods=['GET'])
def index():
    streak = session.get('streak', Streak())
    session["streak"] = streak
    return render_template('index.html', cards=streak.queue, beststreak=streak.best_streak_length, streak=streak.current_streak_length)

@app.route('/newcard')
def newcard():
    print(request.args)
    choice = request.args.get('choice', 'error')
    streak = session["streak"]
    current_card, new_card, best_streak_length, correct = streak.new_card(choice)
    print('Best Streak = ' + str(best_streak_length))
    session["streak"] = streak
    return jsonify({"new_card":new_card, "current_streak_length":streak.current_streak_length, "current_card":current_card, "best_streak_length":best_streak_length, "correct":correct})

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/history')
def history():
    return render_template('history.html')