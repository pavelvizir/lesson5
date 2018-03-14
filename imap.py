#!/usr/bin/env python
''' Try to get mail from gmail '''


from imapclient import IMAPClient
from imap_credentials import imap_username, imap_password


# import logging
# logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
#                     level=logging.DEBUG )


server = IMAPClient('imap.gmail.com', use_uid=True)
server.login(imap_username, imap_password)
select = server.select_folder('INBOX', readonly=True)
print(select)
