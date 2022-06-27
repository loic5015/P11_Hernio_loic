import server
import pytest

@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client

@pytest.fixture
def clubs_fixture():
    data = [{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '13'},
            {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'},
            {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}]
    return data

@pytest.mark.parametrize("email", [("admin@irontemple.com")])
def test_basic_route_test(client, email):
    rv = client.get("/", follow_redirects=True)
    assert rv.status_code == 200
    rv = client.post("/showSummary", data=dict(email=email))
    assert rv.status_code == 200
    rv = client.get("/logout", follow_redirects=True)
    assert rv.status_code == 200

@pytest.mark.parametrize("club, place", [([{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '15'}], 13),
                                         ([{'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'}], 2)])
def test_check_max_point_reached(club, place, clubs_fixture):
    if server.check_max_point_reached(club, place):
        if club[0]['points'] < place:
            assert rv.status_code == 200
            assert rv.data.decode('You have exceeded the maximum number of points allowed').find() != 1
        else:
            assert rv.status_code == 200