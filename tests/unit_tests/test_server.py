import server
import pytest
from pathlib import Path
import os
import datetime

MAX_PLACES_COMPETITION = 12


@pytest.fixture
def competitions_fixture():
    data = [{'name': 'Spring Festival', 'date': '2020-03-27 10:00:00', 'numberOfPlaces': '25'},
            {'name': 'Fall Classic', 'date': '2020-10-22 13:30:00', 'numberOfPlaces': '13'},
            {'name': 'ex competition', 'date': '2023-10-22 13:30:00', 'numberOfPlaces': '13'}]
    return data


@pytest.fixture
def max_places_competitions_fixture():
    data = [{'competition': 'Spring Festival', 'club': 'Iron Temple', 'places': '1'},
            {'competition': 'Fall Classic', 'club': 'Iron Temple', 'places': '6'}]
    return data


@pytest.fixture
def clubs_fixture():
    data = [{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '13'},
            {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'},
            {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}]
    return data

@pytest.fixture
def files_fixture():
    data = [{'file1': 'clubs.json', 'file2': 'competitions.json', 'file3': 'max_places_competition.json'}]
    return data


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client


def test_loadCompetitions(competitions_fixture):
    assert server.loadCompetitions() == competitions_fixture


def test_loadClubs(clubs_fixture):
    assert server.loadClubs() == clubs_fixture


def test_index_code_ok(client):
    response = client.get('/')
    assert response.status_code == 200


def test_logout(client):
    rv = client.get("/logout", follow_redirects=True)
    assert rv.status_code == 200


@pytest.mark.parametrize("email", [("admin@irontemple.com"), ("unknown@gmail.com")])
def test_show_summary(client, email, competitions_fixture):
    rv = client.post("/showSummary", data=dict(email=email))
    assert rv.status_code == 200
    if email == "unknown@gmail.com":
        assert rv.data.decode().find(f'GUDLFT Registration') != -1
    else:
        for competition in competitions_fixture:
            print(competition['date'])
            if datetime.datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S') < datetime.datetime.now():
                assert rv.data.decode().find(f'Competition closed') != -1
            else:
                assert rv.data.decode().find(f'Book Places') != -1


@pytest.mark.parametrize("competition, club", [("Spring Festival", "Iron Temple"), ("Fall Classic", "Iron Temple"),
                                               ("competition inconnu", "club inconnu")])
def test_book(client, clubs_fixture, club, competition):
    rv = client.get(f'book/{competition}/{club}')
    if competition == "competition inconnu"  or club == "club inconnu":
        assert rv.status_code == 404
    else:
        assert rv.status_code == 200


@pytest.mark.parametrize("competition, club, places", [("Spring Festival", "Iron Temple", "1"),
                                                       ("Fall Classic", "Iron Temple", "2"),
                                               ("competition inconnu", "club inconnu", "4")])
def test_purchasePlaces(client, competition, max_places_competitions_fixture,
                        club, places):
    rv = client.post("/purchasePlaces", data=dict(competition=competition, club=club, places=places))
    if competition == "competition inconnu" or club == "club inconnu":
        assert rv.status_code == 404
    else:
        assert rv.status_code == 200
        n = 0
        for max_places_competitions_club in max_places_competitions_fixture:
            if competition == max_places_competitions_club['competition'] and club == max_places_competitions_club['club']\
                    and (int(places) + int(max_places_competitions_club['places'])) > MAX_PLACES_COMPETITION:
                assert rv.data.decode().find(f'Your choice for this competition') != -1
            elif competition == max_places_competitions_club['competition'] and club == max_places_competitions_club['club']\
                    and (int(places) + int(max_places_competitions_club['places'])) <= MAX_PLACES_COMPETITION:
                max_places_competitions_fixture[n]['places'] = str(int(places) + int(max_places_competitions_club['places']))
                assert rv.data.decode().find(f'Great-booking complete!') != -1
            n += 1

def test_files(files_fixture):
    for value in files_fixture[0].values():
        filename = os.path.join(server.app.root_path, value)
        file_obj = Path(filename)
        assert file_obj.is_file() == True


@pytest.mark.parametrize("club, place", [("Simply Lift", 13), ("Iron Temple", 2)])
def test_check_max_point_reached(club, place, clubs_fixture):
    for key, value in clubs_fixture[0].items():
        if key == club:
            if int(value) < place:
                rv = client.post("/showSummary", data=dict(competitions=competitions, club=club, datetime=datetime))
                assert rv.status_code == 200
                assert rv.data.decode('You have exceeded the maximum number of points allowed').find() != 1
            else:
                assert None


def test_index(client):
    rv = client.get("/", follow_redirects=True)
    assert rv.status_code == 200

def test_list_club(client):
    rv = client.get("/list_club", follow_redirects=True)
    assert rv.status_code == 200