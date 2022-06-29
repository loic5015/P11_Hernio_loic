import server
import pytest

COEFFICIENT = 3

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

