from datetime import datetime

from sqlalchemy import and_

from src import db, session
from src import models


def add_contact(owner_id, first_name, last_name, phone_number, email):
    contact = models.Person(first_name=first_name, last_name=last_name,
                            phones=[models.Phone(phone_number=phone_number)],
                            emails=[models.Email(email=email)], owner_id=owner_id)
    session.add(contact)
    session.commit()


def add_person_phone(id):
    phone_number = input("New phone number: ")
    description = input("Description: ")
    phone = models.Phone(phone_number=phone_number, description=description, person_id=id)
    session.add(phone)
    session.commit()


def add_person_email(id):
    email = input("New email: ")
    description = input("Description: ")
    em = models.Email(email=email, description=description, person_id=id)
    session.add(em)
    session.commit()


def remove_phone_number(id):
    phone = session.query(models.Phone).filter(models.Phone.id == id).first()
    session.delete(phone)
    session.commit()


def remove_email(id):
    email = session.query(models.Email).filter(models.Email.id == id).first()
    session.delete(email)
    session.commit()


def update_contact(id):
    person = session.query(models.Person).filter(models.Person.id == id).first()

    fn = input(f'first_name [{person.first_name}]:')
    if fn:
        person.first_name = fn

    ln = input(f'last_name [{person.last_name}]:')
    if ln:
        person.last_name = ln

    for phone in person.phones:
        ph = input(f'phone_number [{phone.phone_number}/del]:')
        if ph == 'del':
            remove_phone_number(phone.id)
            continue
        if ph:
            phone.phone_number = ph
        desc = input(f'phone description [{phone.description}]:')
        if desc:
            phone.description = desc

    while True:
        if input("add phone number [y/n]") == 'y':
            add_person_phone(id)
        else:
            break

    for email in person.emails:
        em = input(f'email [{email.email}/del]:')
        if em == 'del':
            remove_email(email.id)
            continue
        if em:
            email.email = em
        desc = input(f'email description [{email.description}]:')
        if desc:
            email.description = desc

    while True:
        if input("add email [y/n]") == 'y':
            add_person_email(id)
        else:
            break

    bd = input(f'Birth date [{person.birth_date}]:')
    if bd:
        person.birth_date = datetime.strptime(bd, "%d.%m.%y")

    pn = input(f'post [{person.post_name}]:')
    if pn:
        person.post_name = pn

    co = input(f'Company name [{person.work_place}]:')
    if co:
        person.work_place = co

    session.commit()
    return (person.id, person.fullname,
             [(ph.phone_number, ph.description) for ph in person.phones],
             [(em.email, em.description) for em in person.emails],
             person.description)


def get_contact(id):
    person = session.query(models.Person).filter(models.Person.id == id).first()
    return (person.id, person.fullname,
             [(ph.phone_number, ph.description) for ph in person.phones],
             [(em.email, em.description) for em in person.emails],
             person.description)


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
