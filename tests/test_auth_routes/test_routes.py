
def test_healthcheck(client):
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert b"Hello, I'm working!!!" in response.data


def test_healthcheck_wrong_url(client):
    response = client.get("/healthcheck/1")
    assert response.status_code == 404


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


