#!/usr/bin/env python
'''

'''

# from time import time
from flask import Flask, request
from imap_db import db_session, Mail_Account, Mail
from sqlalchemy.exc import OperationalError
from imap_db import create_structure
# from imap import fetch_mails
# from imap import fetch_mails
from imap_populate import create_account, get_mails


app = Flask(__name__)


@app.route('/get_mails')
def create_account_and_download():
    create_account()
    get_mails()
    return 'Maild probably downloaded <a href="http://127.0.0.1:5000/">GO BACK</a>'

@app.route('/create_db')
def create_db():
    create_structure()
    return 'Database should have been created <a href="http://127.0.0.1:5000/">GO BACK</a>'

@app.route('/get_text')
def show_text_email():
    mail_id = int(request.args.get('id'))
    mail = Mail.query.filter(Mail.id == mail_id).first()
    return mail.text

@app.route('/get_html')
def show_html_email():
    mail_id = int(request.args.get('id'))
    mail = Mail.query.filter(Mail.id == mail_id).first()
    return mail.html

@app.route('/')
def show_mails_list():
    '''
    '''
    result = ['<table>']
    result.append('<caption><b>Mails</b></caption>')
    result.extend(['<tr>', '<th>ID</th>', '<th>Text_link</th>',
                           '<th>HTML_link</th>', '</tr>'])
    try:
        mails_list = Mail.query.all()
        if len(mails_list) < 1:
            return 'There are no mails yet <a href="http://127.0.0.1:5000/get_mails">DOWNLOAD</a>'

        for i in mails_list:
            if i.text:
                text = '<a href="http://127.0.0.1:5000/get_text?id={}">link_to_{}_text</a>'.format(i.id, i.id)
            else:
                text = 'not_available_for_some_reason'
            if i.html:
                html = '<a href="http://127.0.0.1:5000/get_html?id={}">link_to_{}_html</a>'.format(i.id, i.id)
            else:
                html = 'not_available_for_some_reason'
            subresult = [
                '<tr>',
                '<td>' + str(i.id) + '</td>',
                '<td>' + text + '</td>',
                '<td>' + html + '</td>',
                '</tr>']
    
            result.extend(subresult)
    
        return '\n'.join(result)
    except OperationalError:
        return 'No database! <a href="http://127.0.0.1:5000/create_db">CREATE</a>'

if __name__ == '__main__':
    app.run()
