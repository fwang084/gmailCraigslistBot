from __future__ import print_function
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from oauth2client import tools

import base64
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
import mimetypes

import httplib2
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

class send_email:
    def __init__(self, service):
        self.service = service
    def create_message(self, sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'rw': base64.urlsafe_b64encode(message.as_bytes())}