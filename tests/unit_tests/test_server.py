import server
import pytest
from pathlib import Path
import os
import datetime


@pytest.fixture
def competitions_fixture():
    data = [{'name': 'Spring Festival', 'date': '2020-03-27 10:00:00', 'numberOfPlaces': '25'},
            {'name': 'Fall Classic', 'date': '2020-10-22 13:30:00', 'numberOfPlaces': '13'}]
    return data


@pytest.fixture
def clubs_fixture():
    data = [{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '13'},
            {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'},
            {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}]
    return data

@pytest.fixture
def files_fixture():
    data = [{'file1': 'clubs.json', 'file2': 'competitions.json'}]
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
    for competition in competitions_fixture:
        print(competition['date'])
        if datetime.datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S') < datetime.datetime.now():
            assert rv.data.decode().find(f'competition closed') != -1
        else:
            assert  rv.data.decode().find(f'Book Places') != -1


@pytest.mark.parametrize("competition, club", [("Spring Festival", "Iron Temple"), ("Fall Classic", "Iron Temple"),
                                               ("competition inconnu", "club inconnu")])
def test_book(client, competitions_fixture, clubs_fixture, club, competition):
    clubs = clubs_fixture
    competitions = competitions_fixture
    rv = client.get(f'book/{competition}/{club}')
    assert rv.status_code == 200


@pytest.mark.parametrize("competition, club, places", [("Spring Festival", "Iron Temple", "1"),
                                                       ("Fall Classic", "Iron Temple", "2"),
                                               ("competition inconnu", "club inconnu", "4")])
def test_purchasePlaces(client, competitions_fixture, clubs_fixture, competition, club, places):
    clubs = clubs_fixture
    competitions = competitions_fixture
    rv = client.post("/purchasePlaces", data=dict(competition=competition, club=club, places=places))
    assert rv.status_code == 200


def test_files(files_fixture):
    filename = os.path.join(server.app.root_path, files_fixture[0]['file1'])
    file_obj = Path(filename)
    assert file_obj.is_file() == True
    filename1 = os.path.join(server.app.root_path, files_fixture[0]['file2'])
    file_obj1 = Path(filename1)
    assert file_obj1.is_file() == True
