from datetime import datetime

from flask_sqlalchemy.model import Model
from sqlalchemy import ForeignKey, Column, Integer, String, Date
from sqlalchemy.event import listens_for
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from src import db


class Owner(db.Model):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    login = Column(String(120), nullable=False)
    hash = Column(String(255), nullable=False)
    email = Column(String(120), nullable=False)
    token_cookie = Column(String(255), nullable=True, default=None)
    persons = relationship('Person', back_populates='owner', cascade='all,delete')



class Person(db.Model):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    birth_date = Column('birth_date', Date, nullable=True)
    work_place = Column(String(120), nullable=True)
    post_name = Column(String(120), nullable=True)
    owner_id = Column(Integer, ForeignKey('owners.id', ondelete="CASCADE"))
    owner = relationship(Owner)
    phones = relationship('Phone', back_populates='person', cascade='all,delete')
    emails = relationship('Email', back_populates='person', cascade='all,delete')

    @hybrid_property
    def fullname(self):
        return self.first_name + ' ' + self.last_name

    @hybrid_property
    def description(self):
        desc = ""
        if self.post_name:
            desc += "Post: " + str(self.post_name) + "\n"
        if self.post_name:
            desc += 'Company: ' + str(self.work_place) + "\n"
        if self.birth_date:
            desc += "Birthday: " + str(self.birth_date) + "\n"
        return desc

    def modify_name(self):
        if not self.first_name[:4] == 'пан ':
            self.first_name = f'пан {self.first_name}'
        return self.first_name


class Phone(db.Model):
    __tablename__ = "phones"
    id = db.Column(Integer, primary_key=True)
    phone_number = Column('phone_number', String(120), nullable=False)
    description = Column('description', String(120), nullable=True)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"))
    person = relationship(Person)


class Email(db.Model):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    email = Column('phone_number', String(120), nullable=False)
    description = Column('description', String(120), nullable=True)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"))
    person = relationship(Person)


@listens_for(Person, "before_insert")
def my_on_connect(mapper, connect, target: Person):
    target.modify_name()


@listens_for(Person, "before_update")
def my_on_connect(mapper, connect, target: Person):
    target.modify_name()
