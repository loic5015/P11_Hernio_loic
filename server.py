import json
from flask import Flask,render_template,request,redirect,flash,url_for
import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club_list = [club for club in clubs if club['email'] == request.form['email']]
    if not club_list:
        flash("Something went wrong-Email unknow")
        return render_template('index.html')
    return render_template('welcome.html',club=club_list[0],competitions=competitions, datetime=datetime)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if not foundClub or not foundCompetition:
        return render_template('404.html', title='404'), 404
    else:
        return render_template('booking.html', club=foundClub[0], competition=foundCompetition[0])


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']]
    club = [c for c in clubs if c['name'] == request.form['club']]
    if not club or not competition:
        return render_template('404.html', title='404'), 404
    else:
        placesRequired = int(request.form['places'])
        competition[0]['numberOfPlaces'] = int(competition[0]['numberOfPlaces'])-placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club[0], competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))