#!/usr/bin/env python
''' Create structure and populate two tables '''

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
import sqlite3

engine = create_engine('sqlite:///mail.sqlite')

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
db_session = Session()

Base = declarative_base()
Base.query = Session.query_property()


class Mail_Account(Base):
    __tablename__ = 'mail_accounts'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    server = Column(String(100), nullable=False)
    port = Column(Integer, default=993)
    last_uid = Column(Integer)

    def __init__(self, email=None, password=None, server=None, port=None):
        self.email = email
        self.password = password
        self.server = server
        self.port = port

    def __repr__(self):
        return '<Mail Account {} {} {} {}>'.format(self.email, self.server, self.port, self.last_uid)


class Mail(Base):
    __tablename__ = 'mails'
    id = Column(Integer, primary_key=True)
    _delivered_to = Column(String(100), ForeignKey('mail_accounts.email'))
    _to = Column(String(200))
    _from = Column(String(200))
    _subject = Column(String(500))
    _date = Column(DateTime)
    _message_id = Column(String(200))
    text = Column(Text)
    html = Column(Text)

    def __init__(self, _delivered_to=None, _to=None, _from=None, _subject=None,
                 _date=None, _message_id=None, text=None, html=None):
        self._delivered_to = _delivered_to
        self._to = _to
        self._from = _from
        self._subject = _subject
        self._date = _date
        self._message_id = _message_id
        self.text = text
        self.html = html

    def __repr__(self):
        return 'Mail {} {} {}'.format(self._to, self._from, self._date)


def create_structure():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    con = sqlite3.connect('mail.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    d = cursor.fetchall()
    for i in d:
        for a in i:
            b = cursor.execute("PRAGMA table_info('{}')".format(a))
            for c in b:
                print(c)

