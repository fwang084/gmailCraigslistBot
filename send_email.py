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

import httplib2
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None