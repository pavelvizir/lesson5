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
import imaplib
from email.contentmanager import ContentManager
from email.parser import BytesHeaderParser, BytesParser
from email.policy import default
import email

from bs4 import BeautifulSoup

from imap_credentials import imap_password, imap_username

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(imap_username, imap_password)
mail.select(mailbox='INBOX', readonly=True)

#_, data = mail.search(None, '(ALL)')
#print(mail.list())
typ, data = mail.search(None, 'SINCE 13-Mar-2018')
#print(len(data))
#print(typ, data)
# print(data[0].[])
"""
for uid in data[0].split()[::-1]:
    # typ1, data1 =    mail.fetch(uid, 'BODY.PEEK[HEADER]')
    # print(uid, typ1, data1)
    typ1, data1 = mail.fetch(
        uid, 'BODY.PEEK[HEADER.FIELDS (FROM TO DATE SUBJECT MESSAGE-ID CC BCC)]')
    #(a, (b, c)) =    data1
    #print(typ1, a, b, c)
    a, b = data1[0]
    # print(a)
    #print(a, b)
    # for i in b.split(b'\r\n'):
    #   print(
    headers = BytesHeaderParser(policy=default).parsebytes(b)
    #print(headers)
    #typ2, data2=    mail.fetch(uid, 'BODY.PEEK[TEXT]')
    typ2, data2 = mail.fetch(uid, '(RFC822)')
    a2, b2 = data2[0]
    body = BytesParser(policy=default).parsebytes(b2)
    # print(body)
    # print(body.get_body()['content-type'])
'''
    print(body.get_body().items())
    for part in body.walk():
        print(part.get_content_type())
    print(body.get('text/html'))
'''
"""
result, data = mail.uid('search', None, "ALL")
# search and return uids instead
# i = len(data[0].split())  # data[0] is a space separate string
# print(i)
latest_email_uid = data[0].split()[13]
result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
raw_email = email_data[0][1]
raw_email_string = raw_email.decode('utf-8')
email_message = email.message_from_string(raw_email_string)
for part in email_message.walk():
    if part.get_content_type() == 'text/plain':
        body = part.get_payload(decode=True)
        print(body.decode())


'''

for x in range(i):
        latest_email_uid = data[0].split()[x] # unique ids wrt label selected
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        # fetch the email body (RFC822) for the given ID
        raw_email = email_data[0][1]
        #continue inside the same for loop as above
        raw_email_string = raw_email.decode('utf-8')
        # converts byte literal to string removing b''
        email_message = email.message_from_string(raw_email_string)
        # this will loop through all the available multiparts in mail
        for part in email_message.walk():
            if part.get_content_type() == "text/plain": # ignore attachments/html
                body = part.get_payload(decode=True)
                save_string = str("D:Dumpgmailemail_" + str(x) + ".eml")
                # location on disk
                myfile = open(save_string, 'a')
                myfile.write(body.decode('utf-8'))
                # body is again a byte literal
                myfile.close()
            else:
                continue


#    print(body.get_body('plain'))
##    pretty = BeautifulSoup(body.get_body(), 'html5lib').get_text()
##    print(pretty)
    

    body2 = body.get_content()
    st = body2.find('<html')
    st2 = body2.rfind('/html>', st) + 6
    body3 = body2[st:st2]
    #body4 =    body.get_content()
    # print(body.get_content())
    # for t in body:
    #   print(body[t])
    # print(body4['content-type'].maintype)
    # print(body.get_body())

    #pretty =    BeautifulSoup(body3, 'html.parser').prettify()
    #pretty2 = BeautifulSoup(body3, 'html.parser').get_text()
    pretty = BeautifulSoup(body3, 'html5lib').get_text()
    print(pretty)
    # print(type(body))
    #body2 =    body.get_body()
    # print(body2['content-type'].maintype)
    # body3 =    ContentManager.get_content(body)
    # print(body3)

    break

    'Delivered-To', 'Received', 'From'


import getpass, imaplib

M = imaplib.IMAP4()
M.login(getpass.getuser(), getpass.getpass())
M.select()
typ, data = M.search(None, 'ALL')

for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    print('Message %s\n%s\n' % (num, data[0][1]))
M.close()
M.logout()





imap_conn.select('Inbox', readonly=True)
typ, msg_data = imap_conn.fetch(uid, '(BODY.PEEK[HEADER])')
or BODY.PEEK[TEXT], etc.
'''