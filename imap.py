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
from datetime import datetime


def fetch_emails(addr, port, user, pwd, uid=None):
    ''' returns up to 5 new emails from INBOX '''
    
    def fetch_and_parse(uids):
        ''' fetches and parses up to 5 new emails '''
        
        res = list()
        for id in uids:
            email_dict = dict()
            result, email_data = imap_server.uid('fetch', id, '(RFC822)')
            raw_email = email_data[0][1]
            email = BytesParser(policy=default).parsebytes(raw_email)
            headers = dict()
            headers['Date'] = datetime.strptime(email['Date'], '%a, %d %b %Y %H:%M:%S %z')
            for header in ['From', 'To', 'Delivered-To',
                                     'Message-ID', 'Subject']:
                headers[header] = email[header]
            email_dict['headers'] = headers
            for part in email.walk():
                if part.get_content_type() == 'text/html':
                    email_dict['html'] = part.get_body().get_content()
                elif part.get_content_type() == 'text/plain':
                    email_dict['plain'] = part.get_body().get_content()
            res.append(email_dict)
        #print(len(res))
            #print(datetime.strptime(email_dict['headers']['Date'], '%a, %d %b %Y %H:%M:%S %z'))
            #print(email_dict['headers'].values())
            print(email_dict['headers']['Date'])
        return res
        
    imap_server = IMAP4_SSL('imap.gmail.com')
    imap_server.login(imap_username, imap_password)
    imap_server.select(mailbox='INBOX', readonly=True)
    if uid:
        result, data = imap_server.uid('search', None, '{}:*'.format(uid))
    else:
        result, data = imap_server.uid('search', None, 'ALL')
        uid = 0
    if result == 'OK':
        uids_blist = data[0].split()
        if len(uids_blist) < 2:
            if uids_blist[0] > str(uid).encode():
                fetch_and_parse(uids_blist)
                return '1 new mail'
            else:
                return '0 new mails'
        elif len(uids_blist) > 5:
            if len(uids_blist) > 10:
                fetch_and_parse(uids_blist[-10:][:5])
            else:
                fetch_and_parse(uids_blist[:5])
            return 'Many new mails'
        else:
            fetch_and_parse(uids_blist)
            return 'Some new mails'
    else:
        return 'Something wrong'


if __name__ == '__main__':
    print(fetch_emails('imap.gmail.com', 993, imap_username, imap_password, 17))
    print(fetch_emails('imap.gmail.com', 993, imap_username, imap_password, 16))
    print(fetch_emails('imap.gmail.com', 993, imap_username, imap_password, 15))
    print(fetch_emails('imap.gmail.com', 993, imap_username, imap_password, 10))
    print(fetch_emails('imap.gmail.com', 993, imap_username, imap_password))
