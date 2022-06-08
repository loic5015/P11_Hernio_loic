import server
import pytest


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
def test_show_summary_email(client, email):
    rv = client.post("/showSummary", data=dict(email=email))
    assert rv.status_code == 200



