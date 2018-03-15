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
структура таблиц емэйл, хранить ли последн message-id
первичная загрузка, если пустая таблица
(обратный порядок, break если сообщение есть?)

'''
from imaplib import IMAP4_SSL
from email.policy import default
from email.parser import BytesParser
from imap_credentials import imap_password, imap_username


def fetch_emails(addr, port, user, pwd, uid=None):
    uid = uid or 1
    imap_server = IMAP4_SSL('imap.gmail.com')
    imap_server.login(imap_username, imap_password)
    imap_server.select(mailbox='INBOX', readonly=True)
    # result, data = mail.uid('search', None, "ALL")
    result, data = imap_server.uid('search', None, '{}:*'.format(uid))
    if result == 'OK':
        if len(data[0].split()) < 2:
            if data[0].split()[0] == str(uid).encode():
                return 'No new emails', len(data[0].split()), data[0]
            elif data[0].split()[0] <= str(uid).encode():
                return 'wtf', result, data
            else:
                return '1 mail'
        else:
            return 'multiple new mails', result, data, len(data[0].split())
    else:
        return 'Something wrong'

'''
    latest_email_uid = data[0].split()[13]
    result, email_data = imap_server.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = email_data[0][1]
    body = BytesParser(policy=default).parsebytes(raw_email)
    print(body['Date'])
    for part in body.walk():
        if part.get_content_type() == 'text/html':
            html = part.get_body().get_content()
        elif part.get_content_type() == 'text/plain':
            txt2 = part.get_body().get_content()
'''

if __name__ == '__main__':
    print(fetch_emails('imap.gmail.com', 993, imap_username, imap_password, 17))
    print(fetch_emails('imap.gmail.com', 993, imap_username, imap_password, 16))
    print(fetch_emails('imap.gmail.com', 993, imap_username, imap_password, 15))
    print(fetch_emails('imap.gmail.com', 993, imap_username, imap_password, 10))
    print(fetch_emails('imap.gmail.com', 993, imap_username, imap_password))
