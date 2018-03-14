from imapclient import IMAPClient
from imap_credentials import imap_username, imap_password

#from imapclient.tls import IMAP4_TLS
#import cryptography
#from OpenSSL import crypto, SSL

import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG ) 


server = IMAPClient('imap.gmail.com', use_uid=True)
#server = IMAP4_TLS('imap.gmail.com', 993, )
server.login(imap_username, imap_password)
#server.login()
select = server.select_folder('INBOX', readonly=True)
print(select)
