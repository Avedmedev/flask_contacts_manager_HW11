import bcrypt

from src import models, session


def create_owner(email, password, nick):
    owner = models.Owner(
        login=nick,
        hash=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10)),
        email=email,
    )
    session.add(owner)
    session.commit()


def login(email, password):
    owner = session.query(models.Owner).filter(models.Owner.email == email).first()

    if not owner:
        return None

    if bcrypt.checkpw(password.encode("utf-8"), owner.hash):
        return owner
    else:
        return None


def set_token(owner, token):
    owner.token_cookie = token
    session.commit()
