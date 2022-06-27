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

def loadMaxPlacesCompetition():
    with open('max_places_competition.json') as comps:
         listOfMaxPlacesCompetitions = json.load(comps)['max_places_competition']
         return listOfMaxPlacesCompetitions

def saveMaxPlacesCompetition(max_places):
    with open('max_places_competition.json', 'w') as comps:
         json.dump(max_places, comps)


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
max_places_competition = loadMaxPlacesCompetition()

MAX_PLACES_COMPETITION = 12
COEFFICIENT = 1

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
        n = 0
        placesRequired = int(request.form['places'])
        if check_max_point_reached(club, placesRequired):
            return render_template('welcome.html', club=club[0], competitions=competitions, datetime=datetime)
        if max_place_competition_reached(competition, placesRequired):
            return render_template('welcome.html', club=club[0], competitions=competitions, datetime=datetime)
        club_and_competition_find = False
        for max_places_competitions_club in max_places_competition:
            if competition[0]["name"] == max_places_competitions_club['competition'] and club[0]["name"] == max_places_competitions_club['club']:
                if placesRequired + int(max_places_competitions_club['places']) > MAX_PLACES_COMPETITION:
                    flash(f'Your choice for this competition exceeds the number of places available for your club')
                    return render_template('welcome.html', club=club[0], competitions=competitions, datetime=datetime)
                else:
                    max_places_competition[n]['places'] = placesRequired + int(max_places_competitions_club['places'])
                    competition[0]['numberOfPlaces'] = int(competition[0]['numberOfPlaces']) - placesRequired
                    flash('Great-booking complete!')
                    max_places = {}
                    max_places['max_places_competition'] = max_places_competition
                    saveMaxPlacesCompetition(max_places)
                    club = update_points_versus_place(club, placesRequired)
                    club_and_competition_find = True
            n += 1
        if not club_and_competition_find:
            if placesRequired <= MAX_PLACES_COMPETITION:
                record_new = {}
                record_new['places'] = placesRequired
                record_new['competition'] = competition[0]["name"]
                record_new['club'] = club[0]["name"]
                max_places_competition.append(record_new)
                competition[0]['numberOfPlaces'] = int(competition[0]['numberOfPlaces']) - placesRequired
                flash('Great-booking complete!')
                max_places = {}
                max_places['max_places_competition'] = max_places_competition
                saveMaxPlacesCompetition(max_places)
                club = update_points_versus_place(club, placesRequired)
            else:
                flash(f'Your choice for this competition exceeds the number of places available for your club')
        return render_template('welcome.html', club=club[0], competitions=competitions, datetime=datetime)


def check_max_point_reached(club, placesRequired):
    if int(club[0]['points']) < placesRequired*COEFFICIENT:
        flash(f'You have exceeded the maximum number of points allowed !!')
        return True

def max_place_competition_reached(competition, places):
    if int(competition[0]["numberOfPlaces"]) < places:
        flash(f'The number of places requested exceeds the number of places remaining for the competition!')
        return True


def update_points_versus_place(club, placesRequired):
    club[0]['points'] = str(int(club[0]['points']) - placesRequired * COEFFICIENT)
    return club

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))