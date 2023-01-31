import pytest
from flask import url_for


def test_login_get_no_auth(app_with_data):
    response = app_with_data.get(url_for('login'))

    assert response.status_code == 200
    cookies = response.headers.getlist("Set-Cookie")
    assert cookies == []


def test_login_post_owner(app_with_data):
    response = app_with_data.post(url_for("login"),
                                  data={
                                      "email": "alex@i.ua",
                                      "password": "12345",
                                      "remember": "on"
                                  })
    assert response.status_code == 302

    cookies = response.headers.getlist("Set-Cookie")
    assert cookies
    session_list = list(filter(lambda x: "session" in x, cookies))
    assert session_list
    session_string = session_list[0].split(";")[0]
    session = session_string.split("=")[1]
    assert session
    username_list = list(filter(lambda x: "username" in x, cookies))
    assert username_list
    username_string = username_list[0].split(";")[0]
    username = username_string.split("=")[1]
    assert username


def test_login_post_owner_remember_off(app_with_data):
    response = app_with_data.post(url_for("login"),
                                  data={
                                      "email": "alex@i.ua",
                                      "password": "12345",
                                      "remember": "off"
                                  })
    assert response.status_code == 302

    cookies = response.headers.getlist("Set-Cookie")
    assert cookies
    username_list = list(filter(lambda x: "username" in x, cookies))
    assert username_list == []


@pytest.mark.parametrize(
    "email, password, message",
    [
        ("alex@i.ua", "1", "password: [&#39;Shorter than minimum length 4.&#39;]"),
        ("alex@i", "112345621", "email: [&#39;Not a valid email address.&#39;]"),
        ("alex@i.ua", "112345621", "err: Invalid credentials. Go to administration"),
    ]
)
def test_login_post_wrong_data(app_with_data, email, password, message):
    response = app_with_data.post(url_for("login"),
                                  data={
                                      "email": email,
                                      "password": password
                                  })

    assert response.status_code == 200
    assert message in response.text


def test_login_get_after_auth(app_with_data):
    response = app_with_data.get(url_for('login'))

    assert response.status_code == 302
    cookies = response.headers.getlist("Set-Cookie")
    assert cookies == []


def test_logout_get_after_auth(app_with_data):
    response = app_with_data.get(url_for('logout'))

    assert response.status_code == 302
    cookies = response.headers.getlist("Set-Cookie")
    assert cookies
    session_list = list(filter(lambda x: "session" in x, cookies))
    assert session_list
    session_string = session_list[0].split(";")[0]
    session = session_string.split("=")[1]
    assert session == ""


def test_logout_get_after_logout(app_with_data):
    response = app_with_data.get(url_for('logout'))

    assert response.status_code == 302

    cookies = response.headers.getlist("Set-Cookie")
    assert cookies == []
