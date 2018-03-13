
import imaplib

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(username, password)
mail.select(mailbox='INBOX', readonly=True)

#_, data = mail.search(None, '(ALL)')
mail.list()


'''
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