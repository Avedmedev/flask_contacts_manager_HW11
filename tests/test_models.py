from src.models import Owner


def test_new_owner():
    owner = Owner(login='Vasia', email='pupkin@i.ua', hash='FlaskIsAwesome')
    assert owner.email == 'pupkin@i.ua'
    assert owner.hash == 'FlaskIsAwesome'
    assert owner.login == 'Vasia'
