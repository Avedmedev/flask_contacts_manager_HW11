import re

import pytest
from flask import url_for

from tests.conftest import CONTACTS


def test_get_contacts_no_auth(app_with_db):

    response = app_with_db.get(url_for("contacts"))

    assert response.status_code == 302


@pytest.mark.parametrize(
    "first_name, last_name, phone_number, email",
    CONTACTS
)
def test_add_contacts(app_with_data, first_name, last_name, phone_number, email):

    from tests.test_auth_routes.test_routes_login import test_login_post_owner
    test_login_post_owner(app_with_data)

    response = app_with_data.post(url_for("contacts_add"),
                                  data={
                                      "first_name": first_name,
                                      "last_name": last_name,
                                      "phone_number": phone_number,
                                      "email": email
                                  })

    assert response.status_code == 302

    response = app_with_data.get(url_for("contacts"))

    assert response.status_code == 200

    assert first_name in response.text
    assert last_name in response.text
    assert phone_number in response.text
    assert email in response.text


@pytest.mark.parametrize(
    "first_name, last_name, phone_number, email",
    CONTACTS
)
def test_get_contacts(app_with_data_contacts, first_name, last_name, phone_number, email):

    from tests.test_auth_routes.test_routes_login import test_login_post_owner
    test_login_post_owner(app_with_data_contacts)

    response = app_with_data_contacts.get(url_for("contacts"))

    assert response.status_code == 200

    assert first_name in response.text
    assert last_name in response.text
    assert phone_number in response.text
    assert email in response.text


def test_contact_by_id(app_with_data_contacts):

    from tests.test_auth_routes.test_routes_login import test_login_post_owner
    test_login_post_owner(app_with_data_contacts)

    response = app_with_data_contacts.get(url_for("contacts"))

    urls = re.findall(r'"\/contact\/\d+"', response.text)

    for url in urls:
        response = app_with_data_contacts.get(url.strip('"'))
        assert response.status_code == 200

    urls = re.findall(r'"\/contacts\/edit\/\d+"', response.text)

    for url in urls:
        response = app_with_data_contacts.get(url.strip('"'))
        assert response.status_code == 200

    urls = re.findall(r'"\/contacts\/delete\/\d+"', response.text)

    for url in urls:
        response = app_with_data_contacts.post(url.strip('"'))
        assert response.status_code == 302
        assert "Deleted successfully" in response.text
