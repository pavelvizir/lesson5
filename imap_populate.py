#!/usr/bin/env python
''' Fill authors table '''

from imap_db import db_session, Mail_Account, Mail
from imap_credentials import imap_username, imap_password
import sqlite3
from imap import fetch_emails

def create_account():
    mail_account = Mail_Account(imap_username, imap_password, 'imap.gmail.com')
    if not Mail_Account.query.filter(Mail_Account.email==imap_username).first():
        db_session.add(mail_account)
        db_session.commit()
    
        con = sqlite3.connect('mail.sqlite')
        cursor = con.cursor()
        cursor.execute("Select * from mail_accounts;")
        print(cursor.fetchall())

def get_mails():
    for account in Mail_Account.query.all():
        new_mails = 'Possibly :-)'
        new_uid = account.last_uid
        while new_mails:
            new_uid, new_mails, mail_list = fetch_emails(account.server, account.port, account.email, account.password, new_uid)
            if mail_list:
                for i in mail_list:
                    mail = Mail(i['Delivered-To'], i['To'], i['From'], i['Subject'], i['Date'], i['Message-ID'], i['plain'], i['html'])
                    db_session.add(mail)
                db_session.commit()
        account.last_uid = new_uid
        db_session.commit()


if __name__ == '__main__':
    create_account()
    print(Mail_Account.query.all())
    get_mails()
