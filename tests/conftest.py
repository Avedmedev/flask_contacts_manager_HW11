import bcrypt
import pytest

from myapp import app
from src.models import db, Owner
from src.repository import persons


@pytest.fixture(scope="session")
def flask_app():

    app.config.update({
        "TESTING": True,
    })

    # other setup can go here
    ctx = app.test_request_context()
    ctx.push()

    yield app

    # clean up / reset resources here
    ctx.pop()


@pytest.fixture(scope="session")
def client(flask_app):
    return flask_app.test_client()


@pytest.fixture(scope="session")
def runner(flask_app):
    return flask_app.test_cli_runner()


@pytest.fixture(scope="session")
def app_with_db(client):
    # db.create_all()

    yield client

    # db.drop_all()   # ATTENTION - IT KILL DATABASE


OWNER_ID = None


@pytest.fixture
def app_with_data(app_with_db):
    owner = Owner()
    owner.login = 'Alex'
    owner.email = 'alex@i.ua'
    owner.hash = bcrypt.hashpw("12345".encode("utf-8"), bcrypt.gensalt(rounds=10))
    db.session.add(owner)

    db.session.commit()

    db.session.refresh(owner)

    global OWNER_ID

    OWNER_ID = owner.id

    yield app_with_db

    db.session.delete(owner)
    db.session.commit()


CONTACTS = [
    ("Vasyl", "Pupko", "2154321843", "ajsdn@sdf.sd"),
    ("Petro", "Poroshko", "6351341515", "asdfg@sas.ua"),
    ("Vova", "Zilvova", "3153121512", "ajasd@com.us"),
]


@pytest.fixture
def app_with_data_contacts(app_with_data):

    for contact in CONTACTS:
        persons.add_contact(OWNER_ID, *contact)

    yield app_with_data

    # for contact in persons.get_persons_owner(OWNER_ID):
    #     db.session.delete(contact.id)
    # db.session.commit()
