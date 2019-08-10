from __future__ import print_function
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from oauth2client import tools

import httplib2
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE  = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python'
authInst = auth.auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.get_credentials()

http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)

import send_email

sendInstance = send_email.send_email(service)
message = sendInstance.create_message('frankw084084@gmail.com', 'frankw084084@gmail.com', 'Test', 'Hi')
sendInstance.send_message('me', message)