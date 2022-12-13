from sqlalchemy import and_

from src import db, session
from src import models


def add_contact(owner_id, first_name, last_name, phone_number, email):
    contact = models.Person(first_name=first_name, last_name=last_name,
                            phones=[models.Phone(phone_number=phone_number)],
                            emails=[models.Email(email=email)], owner_id=owner_id)
    session.add(contact)
    session.commit()


def get_persons_owner(owner_id):
    contacts = session.query(models.Person).filter(models.Person.owner_id == owner_id).all()

    return contacts


def delete_contact_owner(owner_id, contact_id):
    contact = session.query(models.Person).filter(and_(models.Person.id == contact_id,
                                                       models.Person.owner_id == owner_id)).first()
    session.delete(contact)
    session.commit()


def get_contact_user(owner_id, contact_id):
    contact = session.query(models.Person).filter(and_(models.Person.id == contact_id,
                                                       models.Person.owner_id == owner_id)).first()
    return contact


def update_person(contact_id, owner_id, first_name, last_name, phone_number, email):
    contact = get_contact_user(owner_id, contact_id)
    contact.first_name = first_name
    contact.last_name = last_name
    session.commit()
    phone = session.query(models.Phone).filter(models.Phone.person_id == contact_id).first()
    phone.phone_number = phone_number
    session.commit()
    em = session.query(models.Email).filter(models.Email.person_id == contact_id).first()
    em.email = email
    session.commit()


