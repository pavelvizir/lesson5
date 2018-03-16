#!/usr/bin/env python
''' проверка deleted
async
time format utc this day
check sent as well
create lib providers email
/ module structure
следует ли хранить пароль в базе, может хэш соль
или вообще в конфиг...
следует ли создавать для адресатов записи в email_meta
первичная загрузка, если пустая таблица
logout?
'''
from datetime import datetime
from email.parser import BytesParser
from email.policy import default
from imaplib import IMAP4_SSL

from imap_credentials import imap_password, imap_username


def fetch_emails(addr, port, user, pwd,
                 uid=None, mail_limit=10, commit_limit=5):
    ''' returns up to "commit_limit" new emails from INBOX per run
        touches no more than "mail_limit" mails per multiple runs'''

    def fetch_and_parse(uids):
        ''' fetches and parses up to "commit_limit" new emails '''

        result = list()

        for uid in uids:
            email_dict = dict()
            reply, email_data = imap_server.uid('fetch', uid, '(RFC822)')
            if reply == 'OK':
                raw_email = email_data[0][1]
                email = BytesParser(policy=default).parsebytes(raw_email)
                email_dict['Date'] = datetime.strptime(
                    email['Date'], '%a, %d %b %Y %H:%M:%S %z')

                for header in ['From', 'To', 'Delivered-To',
                               'Message-ID', 'Subject']:
                    email_dict[header] = email[header]

                for part in email.walk():
                    if part.get_content_type() == 'text/html':
                        email_dict['html'] = part.get_body().get_content()
                    elif part.get_content_type() == 'text/plain':
                        email_dict['plain'] = part.get_body().get_content()
                result.append(email_dict)
                print(email_dict['Date'])

        return result

    imap_server = IMAP4_SSL('imap.gmail.com')
    imap_server.login(imap_username, imap_password)
    imap_server.select(mailbox='INBOX', readonly=True)

    if uid:
        reply, data = imap_server.uid('search', None, '{}:*'.format(uid))
    else:
        reply, data = imap_server.uid('search', None, 'ALL')
        uid = 0

    if reply == 'OK':
        uids_blist = data[0].split()
        len_uids_blist = len(uids_blist)

        if len(uids_blist) < 2:
            if uids_blist[0] > str(uid).encode():
                fetch_and_parse(uids_blist)

                return '1 new mail'

            return '0 new mails'
        elif len(uids_blist) > commit_limit:
            if len(uids_blist) > mail_limit:
                fetch_and_parse(uids_blist[-mail_limit:][:commit_limit])
            else:
                fetch_and_parse(uids_blist[:commit_limit])

            return 'Many new mails'
        else:
            fetch_and_parse(uids_blist)

            return 'Some new mails'
    else:
        return 'Something wrong'


if __name__ == '__main__':
    for num in [17, 16, 15, 10, None]:
        print(fetch_emails('imap.gmail.com', 993, imap_username, imap_password, num))
