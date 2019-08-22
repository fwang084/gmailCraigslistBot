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
import craigslist_get as cl
import util as util
import time

url = 'https://sfbay.craigslist.org/search/eby/fua'
sendInstance = send_email.send_email(service)

#Getting user input for interested items
items_budgets = {}
while True:
    item = input("Type an item you are interested in: ")
    budget = int(input("What is the most you are willing to spend on that item (in dollars)? "))
    items_budgets[item] = budget
    another = input("Enter Y to enter another item, N if you are done.")
    if another == "N":
        break
duration = float(input("How many hours do you want to search for?"))
minutes_between_searches = 30
repetitions = round(duration * 60 / minutes_between_searches)
iterations = 0
previous_last_seen = 0
for x in range(repetitions):
    posts = cl.get_posts_on_page(url)
    posts_to_email = []
    current_last_seen = posts[0]
    if iterations == 0:
        for x in range(len(posts)):
            posts_to_email = util.check_post(posts_to_email, post[x], items_budgets)
    else:
        for x in range(len(posts)):
            if posts[x] == previous_last_seen:
                break
            posts_to_email = util.check_post(posts_to_email, post[x], items_budgets)
    util.send_posts(posts_to_email, sendInstance, url)
    util.check_for_failure(posts_to_email, sendInstance)
    previous_last_seen = current_last_seen
    iterations += 1
    time.sleep(minutes_between_searches * 60)
message = sendInstance.create_message('frankw084084@gmail.com', 'frankw084084@gmail.com', 'Searching completed', 'Restart program to resume searching')
sendInstance.send_message('me', message)

